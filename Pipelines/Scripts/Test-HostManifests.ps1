<#
.SYNOPSIS
	Checks that the Codex and Cursor manifests match the Claude manifests.

.DESCRIPTION
	Used by .github/workflows/pr-validation.yml. The Claude manifests are the source of
	truth, because 'claude plugin validate' checks them. Each other host reads its own
	files:

	| Host   | Marketplace                       | Each plugin                      |
	|--------|-----------------------------------|----------------------------------|
	| Claude | .claude-plugin/marketplace.json   | .claude-plugin/plugin.json       |
	| Codex  | .agents/plugins/marketplace.json  | .codex-plugin/plugin.json        |
	| Cursor | .cursor-plugin/marketplace.json   | .cursor-plugin/plugin.json       |

	1. Each marketplace has the same 'name' as the Claude marketplace, and lists the same
	   plugins, in the same order, with the same source path.
	2. Each plugin has a Codex and a Cursor manifest with the same 'name', 'version' and
	   'description' as its Claude manifest. A host that sees an old version does not
	   update.
	3. Each Codex manifest has 'skills' set to './skills/', and the 'interface' fields that
	   Codex requires, within the Codex limits ('displayName' and 'shortDescription' 30
	   characters or fewer).

	No CLI validates the Codex or Cursor files, so this script checks the fields that the
	host documentation names. See Docs/Claude-Plugin-Distribution.md, "Other hosts".

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

# Reads a JSON file, or reports it and returns $null.
function Read-Json {
	param([string]$RelativePath)
	$path = Join-Path $SourcesDirectory $RelativePath
	if (-not (Test-Path -LiteralPath $path)) {
		Write-PipelineError "$RelativePath does not exist."
		return $null
	}
	try {
		return Get-Content -LiteralPath $path -Raw -Encoding UTF8 | ConvertFrom-Json
	} catch {
		Write-PipelineError "${RelativePath}: is not valid JSON: $($_.Exception.Message)"
		return $null
	}
}

# The source path of a marketplace entry: a string, or a Codex '{ source: local, path }' object.
function Get-SourcePath {
	param($Source)
	if ($Source -is [string]) { return $Source }
	if ($Source.source -ceq 'local') { return "$($Source.path)" }
	return $null
}

# --- 1. The marketplaces ----------------------------------------------------------------
$claudeMarketplace = Read-Json '.claude-plugin/marketplace.json'
if (-not $claudeMarketplace) { exit 1 }
$expected = @($claudeMarketplace.plugins | ForEach-Object { "$($_.name) -> $(Get-SourcePath $_.source)" })

foreach ($file in '.agents/plugins/marketplace.json', '.cursor-plugin/marketplace.json') {
	$marketplace = Read-Json $file
	if (-not $marketplace) { continue }
	if ("$($marketplace.name)" -cne "$($claudeMarketplace.name)") {
		Write-PipelineError "${file}: name is '$($marketplace.name)'. Use '$($claudeMarketplace.name)', the name of the Claude marketplace."
	}
	$actual = @($marketplace.plugins | ForEach-Object { "$($_.name) -> $(Get-SourcePath $_.source)" })
	if (($actual -join '; ') -cne ($expected -join '; ')) {
		Write-PipelineError "${file}: lists '$($actual -join '; ')'. Use the plugins of .claude-plugin/marketplace.json, in the same order: '$($expected -join '; ')'."
	}
	if ($file -like '.agents/*') {
		if (-not $marketplace.interface.displayName) { Write-PipelineError "${file}: has no interface.displayName." }
		foreach ($entry in @($marketplace.plugins)) {
			if (-not $entry.policy.installation -or -not $entry.policy.authentication) {
				Write-PipelineError "${file}: the entry '$($entry.name)' needs policy.installation and policy.authentication."
			}
			if (-not $entry.category) { Write-PipelineError "${file}: the entry '$($entry.name)' has no category." }
		}
	}
	Write-Host "Checked: $file ($($actual.Count) plugins)"
}

# --- 2 and 3. The plugin manifests ------------------------------------------------------
foreach ($entry in @($claudeMarketplace.plugins)) {
	$folder = (Get-SourcePath $entry.source) -replace '^\./', ''
	$claude = Read-Json "$folder/.claude-plugin/plugin.json"
	if (-not $claude) { continue }

	foreach ($host_ in 'codex', 'cursor') {
		$file = "$folder/.$host_-plugin/plugin.json"
		$manifest = Read-Json $file
		if (-not $manifest) { continue }
		foreach ($field in 'name', 'version', 'description') {
			if ("$($manifest.$field)" -cne "$($claude.$field)") {
				Write-PipelineError "${file}: $field is '$($manifest.$field)'. Use '$($claude.$field)', the same as $folder/.claude-plugin/plugin.json."
			}
		}
		if (-not $manifest.author.name) { Write-PipelineError "${file}: has no author.name." }

		if ($host_ -eq 'codex') {
			if ("$($manifest.skills)" -cne './skills/') { Write-PipelineError "${file}: skills must be './skills/'." }
			$interface = $manifest.interface
			if (-not $interface) {
				Write-PipelineError "${file}: has no interface."
				continue
			}
			foreach ($field in 'displayName', 'shortDescription', 'longDescription', 'developerName', 'category') {
				if (-not $interface.$field) { Write-PipelineError "${file}: has no interface.$field." }
			}
			foreach ($field in 'displayName', 'shortDescription') {
				if ("$($interface.$field)".Length -gt 30) {
					Write-PipelineError "${file}: interface.$field has $("$($interface.$field)".Length) characters. The maximum is 30."
				}
			}
			if ("$($interface.longDescription)".Length -gt 4000) {
				Write-PipelineError "${file}: interface.longDescription has more than 4000 characters."
			}
			if ($null -eq $interface.capabilities) { Write-PipelineError "${file}: has no interface.capabilities. Use [] for none." }
			if ("$($interface.displayName)" -cne "$($claude.displayName)") {
				Write-PipelineError "${file}: interface.displayName is '$($interface.displayName)'. Use '$($claude.displayName)', the displayName in $folder/.claude-plugin/plugin.json."
			}
		}
		Write-Host "Checked: $file"
	}
}

if ($errors -gt 0) { exit 1 }
