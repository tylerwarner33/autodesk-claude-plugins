<#
.SYNOPSIS
	Checks the Claude Code plugin and marketplace manifests.

.DESCRIPTION
	Used by .github/workflows/pr-validation.yml. Needs the Claude Code CLI ('claude')
	on PATH. 'claude plugin validate' needs no sign-in and no network.

	Runs 'claude plugin validate' on the repository root. Every error and every
	warning in the manifests fails (ex. a missing 'version': Test-Changelog.ps1
	checks that it is the newest CHANGELOG.md version). The plugin directory
	findings (ex. ICON_MISSING) are for a listing in the plugin directory, so they
	do not fail.

	Writes GitHub Actions workflow commands, so errors show on the run summary and
	on the pull request.

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

function Write-PipelineError { param($msg) Write-Host "::error::$msg"; $script:errors++ }

$output   = & claude plugin validate $SourcesDirectory --json 2>&1 | ForEach-Object { "$_" }
$exitCode = $LASTEXITCODE
if ($exitCode -eq 2) {
	Write-PipelineError "claude plugin validate could not run: $($output -join ' ')"
	exit 1
}
try {
	$report = ($output -join "`n") | ConvertFrom-Json
} catch {
	Write-PipelineError "Cannot read the output of claude plugin validate: $($output -join ' ')"
	exit 1
}

foreach ($result in @($report.manifest) + @($report.contents)) {
	if (-not $result) { continue }
	$file = Split-Path $result.file -Leaf
	foreach ($e in @($result.errors)) {
		if ($e) { Write-PipelineError "${file}: $($e.path): $($e.message)" }
	}
	foreach ($w in @($result.warnings)) {
		if ($w) { Write-PipelineError "${file}: $($w.path): $($w.message)" }
	}
}
if ($exitCode -ne 0 -and $errors -eq 0) {
	Write-PipelineError "claude plugin validate failed with exit code $exitCode."
}
Write-Host "Checked: claude plugin validate"

if ($errors -gt 0) { exit 1 }
