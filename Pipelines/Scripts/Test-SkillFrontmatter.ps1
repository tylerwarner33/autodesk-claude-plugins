<#
.SYNOPSIS
	Checks the SKILL.md frontmatter of every skill under skills/.

.DESCRIPTION
	Used by .github/workflows/pr-validation.yml. Fails when a folder under skills/ has
	no SKILL.md, or when a SKILL.md frontmatter breaks the Agent Skills limits.
	Writes GitHub Actions workflow commands, so errors and warnings show on the run
	summary and on the pull request.

	The frontmatter parser reads only the YAML forms that a SKILL.md uses: top-level
	'key: value' lines, quoted values, folded and literal block scalars ('>-', '|'),
	plain values that continue on indented lines, and nested blocks (ex. 'metadata').
	It reports a form that it cannot read as an error, so that a check never passes
	on a value that it did not read.

	The limits are from the Agent Skills specification (https://agentskills.io/specification).
	The reserved words and the XML tag check are from Anthropic's naming rules for skills.

.PARAMETER SourcesDirectory
	The repository root.
#>
[CmdletBinding()]
param(
	[Parameter(Mandatory)]
	[string]$SourcesDirectory
)

$ErrorActionPreference = 'Stop'
$skillsRoot = Join-Path $SourcesDirectory 'skills'
$errors     = 0

# The top-level fields in the Agent Skills specification.
$knownFields = @('name', 'description', 'license', 'compatibility', 'metadata', 'allowed-tools')

function Write-PipelineError { param($msg) Write-Host "::error::$msg"; $script:errors++ }
function Write-PipelineWarning { param($msg) Write-Host "::warning::$msg" }

$folders = @(Get-ChildItem -LiteralPath $skillsRoot -Directory | Select-Object -ExpandProperty Name)
if ($folders.Count -eq 0) {
	Write-PipelineError "The skills/ folder has no skills."
	exit 1
}

# Returns the value of a plain or quoted scalar, without the quotes or a trailing comment.
# Returns $null for a form that the parser does not read.
function ConvertFrom-YamlScalar {
	param([string]$Text)
	$Text = $Text.Trim()
	if ($Text -match '^"((?:[^"\\]|\\.)*)"\s*(#.*)?$') { return [regex]::Unescape($Matches[1]) }
	if ($Text -match "^'((?:[^']|'')*)'\s*(#.*)?$")      { return $Matches[1] -replace "''", "'" }
	if ($Text -match '^[''"]')                           { return $null }   # An unclosed or multi-line quote.
	if ($Text -match '^([\[{&*!|>%@`]|[-?:](\s|$))')    { return $null }   # A flow collection, anchor, alias, tag, or reserved character.
	$Text = ($Text -replace '\s+#.*$', '').Trim()
	if ($Text -match ':(\s|$)')                          { return $null }   # YAML reads ': ' in a plain value as a new mapping.
	return $Text
}

foreach ($name in $folders) {
	$skillFile = Join-Path $skillsRoot "$name/SKILL.md"
	$label     = "skills/$name/SKILL.md"
	if (-not (Test-Path -LiteralPath $skillFile)) {
		Write-PipelineError "'skills/$name' has no SKILL.md."
		continue
	}

	# Read the frontmatter between the first two '---' lines. @() keeps an empty or
	# one-line file an array.
	$lines = @(Get-Content -LiteralPath $skillFile)
	$end   = -1
	if ($lines.Count -gt 0 -and $lines[0] -match '^---\s*$') {
		for ($i = 1; $i -lt $lines.Count; $i++) {
			if ($lines[$i] -match '^---\s*$') { $end = $i; break }
		}
	}
	if ($end -lt 0) {
		Write-PipelineError "'$label' has no YAML frontmatter. It must start with a '---' line, and a second '---' line must close it."
		continue
	}
	if ($end -eq 1) {
		Write-PipelineError "'$label' has empty YAML frontmatter."
		continue
	}

	# $fields holds the text of each top-level key. $nested holds the keys whose value is
	# a block of mappings or a list, and not text. YAML keys are case-sensitive, but a
	# PowerShell hashtable is not, so use an ordinal comparer.
	$fields   = [System.Collections.Specialized.OrderedDictionary]::new([StringComparer]::Ordinal)
	$nested   = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
	$key      = $null
	$block    = $false   # The value of $key is a '>' or '|' block scalar.
	$parseOk  = $true
	for ($i = 1; $i -lt $end; $i++) {
		$line   = $lines[$i]
		$lineNo = $i + 1
		if ($line -match '^\t' -or ($line -match '^ +\t')) {
			Write-PipelineError "'$label' line ${lineNo}: YAML does not allow a tab for indentation."
			$parseOk = $false
			continue
		}
		if ($line -match '^([A-Za-z][\w-]*):(?:\s+(.*))?$') {
			$key   = $Matches[1]
			$value = "$($Matches[2])".Trim()
			if ($fields.Contains($key)) {
				Write-PipelineError "'$label' line ${lineNo}: the key '$key' occurs more than once."
				$parseOk = $false
			}
			$block = $value -match '^[>|][-+]?\d?\s*(#.*)?$'
			if ($block -or $value -eq '' -or $value -match '^#') {
				$fields[$key] = ''
			} else {
				$scalar = ConvertFrom-YamlScalar $value
				if ($null -eq $scalar) {
					Write-PipelineError "'$label' line ${lineNo}: cannot read the value of '$key'. Use plain text, a quoted string, or a '>-' block."
					$parseOk = $false
					$scalar = ''
				}
				$fields[$key] = $scalar
			}
		} elseif ($line -match '^\s*$' -or $line -match '^#') {
			# A blank line, or a comment at the left margin. A blank line in a block scalar adds
			# nothing to the length that the checks need.
			continue
		} elseif ($key -and -not $block -and $line -match '^-(\s|$)' -and ($nested.Contains($key) -or $fields[$key] -eq '')) {
			# YAML allows a list item at the same indentation as its key.
			[void]$nested.Add($key)
		} elseif ($key -and $line -match '^\s+(\S.*)$') {
			$text = $Matches[1]
			# A first indented line that is a list item or a 'key: value' line makes the value a
			# nested block, not text (ex. 'metadata:' followed by '  version: "1.0.0"').
			if (-not $block -and ($nested.Contains($key) -or ($fields[$key] -eq '' -and $text -match '^(-(\s|$)|[\w-]+:(\s|$))'))) {
				[void]$nested.Add($key)
				continue
			}
			if (-not $block) {
				$text = $text -replace '\s+#.*$', ''
				if ($text -match ':(\s|$)') {
					Write-PipelineError "'$label' line ${lineNo}: the value of '$key' contains ': '. Quote the value, or use a '>-' block."
					$parseOk = $false
				}
			}
			$fields[$key] = ("$($fields[$key]) $text").Trim()
		} else {
			Write-PipelineError "'$label' line ${lineNo}: cannot read this line: $line"
			$parseOk = $false
		}
	}
	if (-not $parseOk) { continue }

	foreach ($field in $fields.Keys | Where-Object { $_ -cnotin $knownFields }) {
		Write-PipelineWarning "'$label' has the field '$field', which is not in the Agent Skills specification. Other agents ignore it."
	}
	foreach ($field in @('name', 'description', 'compatibility', 'license') | Where-Object { $nested.Contains($_) }) {
		Write-PipelineError "'$label' field '$field' must be text, not a list or a nested block."
	}

	$skillName   = $fields['name']
	$description = $fields['description']

	if (-not $fields.Contains('name')) {
		Write-PipelineError "'$label' has no name. Add 'name: $name'."
	} elseif (-not $skillName) {
		Write-PipelineError "'$label' has an empty name. Use 'name: $name'."
	} else {
		if ($skillName -cne $name) {
			Write-PipelineError "'$label' has name '$skillName'. The name must be the folder name, '$name'."
		}
		# -cmatch: -match ignores case, so '[a-z]' would also accept capital letters.
		if ($skillName.Length -gt 64 -or $skillName -cnotmatch '^[a-z0-9]+(-[a-z0-9]+)*$') {
			Write-PipelineError "'$label' name must be 64 characters or fewer, with only lowercase letters, digits, and single hyphens between them."
		}
		if ($skillName -match 'anthropic|claude') {
			Write-PipelineError "'$label' name contains a reserved word ('anthropic' or 'claude')."
		}
	}

	if (-not $fields.Contains('description')) {
		Write-PipelineError "'$label' has no description."
	} elseif (-not $description) {
		Write-PipelineError "'$label' has an empty description."
	} elseif ($description.Length -gt 1024) {
		Write-PipelineError "'$label' description has $($description.Length) characters. The maximum is 1024."
	}
	if ($description -match '<[A-Za-z/]') {
		Write-PipelineError "'$label' description contains an XML tag."
	}

	if ($fields.Contains('compatibility') -and -not $nested.Contains('compatibility')) {
		$compatibility = $fields['compatibility']
		if (-not $compatibility) {
			Write-PipelineError "'$label' has an empty compatibility. Remove the field, or give it a value."
		} elseif ($compatibility.Length -gt 500) {
			Write-PipelineError "'$label' compatibility has $($compatibility.Length) characters. The maximum is 500."
		}
	}

	Write-Host "Checked: skills/$name ($("$description".Length)-character description)"
}

if ($errors -gt 0) { exit 1 }
