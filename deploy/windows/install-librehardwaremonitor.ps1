[CmdletBinding()]
param(
    [string]$Destination
)

$ErrorActionPreference = 'Stop'
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
if (-not $Destination) {
    $Destination = Join-Path $ProjectRoot 'vendor\librehardwaremonitor'
}

$Version = '0.9.6'
$ArchiveUrl = 'https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases/download/v0.9.6/LibreHardwareMonitor.zip'
$ExpectedSha256 = '086d9f1b5a99e643edc2cfaaac16051685b551e4c5ac0b32a57c58c0e529c001'
$TempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("server-monitor-lhm-" + [guid]::NewGuid().ToString('N'))
$ArchivePath = Join-Path $TempRoot 'LibreHardwareMonitor.zip'
$ExtractPath = Join-Path $TempRoot 'extracted'

try {
    New-Item -ItemType Directory -Path $TempRoot -Force | Out-Null
    Write-Host "Downloading LibreHardwareMonitor $Version from the official GitHub release..."
    Invoke-WebRequest -Uri $ArchiveUrl -OutFile $ArchivePath
    $ActualSha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $ArchivePath).Hash.ToLowerInvariant()
    if ($ActualSha256 -ne $ExpectedSha256) {
        throw "LibreHardwareMonitor checksum mismatch. Expected $ExpectedSha256, got $ActualSha256."
    }

    Expand-Archive -LiteralPath $ArchivePath -DestinationPath $ExtractPath -Force
    $Library = Get-ChildItem -LiteralPath $ExtractPath -Recurse -File -Filter 'LibreHardwareMonitorLib.dll' |
        Select-Object -First 1
    if (-not $Library) {
        throw 'LibreHardwareMonitorLib.dll was not found in the verified archive.'
    }

    New-Item -ItemType Directory -Path $Destination -Force | Out-Null
    Copy-Item -Path (Join-Path $Library.Directory.FullName '*') -Destination $Destination -Recurse -Force
    Write-Host "LibreHardwareMonitor $Version installed at $Destination"
}
finally {
    $ResolvedTempBase = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
    $ResolvedTempRoot = [System.IO.Path]::GetFullPath($TempRoot)
    if ($ResolvedTempRoot.StartsWith($ResolvedTempBase, [System.StringComparison]::OrdinalIgnoreCase) -and
        (Test-Path -LiteralPath $ResolvedTempRoot)) {
        Remove-Item -LiteralPath $ResolvedTempRoot -Recurse -Force
    }
}
