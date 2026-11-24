<#
.SYNOPSIS
	Checks that each plugin is self-contained, and that the Inventor skills work with
	any tool that drives Inventor.

.DESCRIPTION
	Used by .github/workflows/pr-validation.yml. Reads every Markdown file under
	plugins/*/skills/.

	1. A skill names only the skills of its own plugin. A user can install one plugin
	   without the others, so a name (in backticks) of a skill in another plugin fails.
	2. A skill of an Inventor plugin (plugins/inventor-*) names no tool and no script
	   helper of one Inventor MCP server (ex. 'inventor_health', 'InTransaction'). The
	   skills must work with any server, an add-in, or a plugin, so they name only the
	   Inventor API. The server-specific steps stay with the server.

	Writes GitHub Actions workflow commands, so errors show on the run summary and on
	the pull request.

.PARAMETER SourcesDirectory
	The repository root.
#>
[CmdletBinding()]
param(
	[Parameter(Mandatory)]
	[string]$SourcesDirectory
)

$ErrorActionPreference = 'Stop'
$errors = 0
# .NET resolves a relative path from the process folder, not from the PowerShell location.
$SourcesDirectory = (Resolve-Path -LiteralPath $SourcesDirectory).Path

function Write-PipelineError { param($msg) Write-Host "::error::$msg"; $script:errors++ }

# The tools of an Inventor MCP server are 'inventor_<name>'. The helpers are the script
# globals of the Autodesk Inventor MCP Server (its ScriptPrelude.csx), and the words of
# its results.
$toolPattern = '\binventor_[a-z_]*[a-z]\b'
$serverWords = @(
	'FindOpenDocument', 'OpenOrReuseDocument', 'CloseDocumentsOpenedHere',
	'ILogicAutomation', 'ILogicRuleNames', 'ILogicRuleText', 'SetILogicRuleText', 'RunILogicRule',
	'ToInches', 'FromInches', 'ToMillimeters', 'FromMillimeters', 'ToMillimetres', 'FromMillimetres',
	'ToDegrees', 'FromDegrees',
	'TryGetUserParameter', 'InTransaction', 'ScriptDeadline', 'StartDeadline',
	'blockingDialogs', 'blocked-by-dialog'
)
$serverPattern = '(?<![\w-])(' + (($serverWords | ForEach-Object { [regex]::Escape($_) }) -join '|') + ')(?![\w-])'

# The plugin of each skill, by skill name.
$pluginOfSkill = @{}
foreach ($skill in Get-ChildItem -Path (Join-Path $SourcesDirectory 'plugins/*/skills/*') -Directory) {
	$pluginOfSkill[$skill.Name] = $skill.Parent.Parent.Name
}
if ($pluginOfSkill.Count -eq 0) {
	Write-PipelineError "No plugin under plugins/ has a skill."
	exit 1
}

$checked = 0
foreach ($skill in Get-ChildItem -Path (Join-Path $SourcesDirectory 'plugins/*/skills/*') -Directory) {
	$plugin = $skill.Parent.Parent.Name
	foreach ($file in Get-ChildItem -LiteralPath $skill.FullName -Recurse -File -Filter '*.md') {
		$relative = [System.IO.Path]::GetRelativePath($SourcesDirectory, $file.FullName).Replace('\', '/')
		$lines = @(Get-Content -LiteralPath $file.FullName -Encoding UTF8)
		for ($i = 0; $i -lt $lines.Count; $i++) {
			$n = $i + 1
			foreach ($match in [regex]::Matches($lines[$i], '`([a-z0-9]+(?:-[a-z0-9]+)*)`')) {
				$name = $match.Groups[1].Value
				if ($pluginOfSkill.ContainsKey($name) -and $pluginOfSkill[$name] -ne $plugin) {
					Write-PipelineError "${relative}:${n}: names the skill '$name' of the plugin '$($pluginOfSkill[$name])'. A plugin is installed alone, so name only the skills of '$plugin', or write the fact here."
				}
			}
			if ($plugin -like 'inventor-*') {
				foreach ($match in [regex]::Matches($lines[$i], $toolPattern)) {
					Write-PipelineError "${relative}:${n}: names the MCP server tool '$($match.Value)'. Name the Inventor API member instead."
				}
				foreach ($match in [regex]::Matches($lines[$i], $serverPattern)) {
					Write-PipelineError "${relative}:${n}: names '$($match.Value)', which belongs to one Inventor MCP server. Write the Inventor API calls instead."
				}
			}
		}
		$checked++
	}
}

Write-Host "Checked: $checked skill files in $($pluginOfSkill.Count) skills"
if ($errors -gt 0) { exit 1 }
