[CmdletBinding()]
param(
    [string]$Python,
    [switch]$SkipLibreHardwareMonitor
)

$ErrorActionPreference = 'Stop'
$TaskName = 'Server Monitor'
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$VenvRoot = Join-Path $ProjectRoot 'venv'
$VenvPython = Join-Path $VenvRoot 'Scripts\python.exe'
$VenvPythonw = Join-Path $VenvRoot 'Scripts\pythonw.exe'
$ServerScript = Join-Path $ProjectRoot 'server.py'

function Assert-MinimumPython {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Executable,
        [string[]]$PythonArguments = @()
    )

    & $Executable @PythonArguments -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 9) else 1)'
    if ($LASTEXITCODE -ne 0) {
        $DetectedVersion = (& $Executable @PythonArguments --version 2>&1 | Out-String).Trim()
        throw "Python 3.9 or newer is required. Found: $DetectedVersion"
    }
}

if (-not (Test-Path -LiteralPath $VenvPython)) {
    Write-Host 'Creating the local Python virtual environment...'
    if ($Python) {
        Assert-MinimumPython -Executable $Python
        & $Python -m venv $VenvRoot
    }
    elseif (Get-Command py -ErrorAction SilentlyContinue) {
        Assert-MinimumPython -Executable 'py' -PythonArguments @('-3')
        & py -3 -m venv $VenvRoot
    }
    elseif (Get-Command python -ErrorAction SilentlyContinue) {
        Assert-MinimumPython -Executable 'python'
        & python -m venv $VenvRoot
    }
    else {
        throw 'Python 3 was not found. Install Python or pass -Python C:\path\to\python.exe.'
    }
}

Assert-MinimumPython -Executable $VenvPython

& $VenvPython -m pip install --upgrade 'pip==26.0.1'
& $VenvPython -m pip install -r (Join-Path $ProjectRoot 'requirements.txt')

if (-not $SkipLibreHardwareMonitor) {
    & (Join-Path $PSScriptRoot 'install-librehardwaremonitor.ps1')
}

$CurrentIdentity = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$Action = New-ScheduledTaskAction `
    -Execute $VenvPythonw `
    -Argument ('"{0}"' -f $ServerScript) `
    -WorkingDirectory $ProjectRoot
$Trigger = New-ScheduledTaskTrigger -AtLogOn -User $CurrentIdentity
$Principal = New-ScheduledTaskPrincipal `
    -UserId $CurrentIdentity `
    -LogonType Interactive `
    -RunLevel Limited
$TaskSettings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit ([TimeSpan]::Zero) `
    -MultipleInstances IgnoreNew `
    -RestartCount 999 `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -StartWhenAvailable

$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($ExistingTask) {
    Stop-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
}
Register-ScheduledTask `
    -TaskName $TaskName `
    -Description 'Server Monitor backend for the current user' `
    -Action $Action `
    -Trigger $Trigger `
    -Principal $Principal `
    -Settings $TaskSettings `
    -Force | Out-Null
Start-ScheduledTask -TaskName $TaskName

$Healthy = $false
for ($Attempt = 0; $Attempt -lt 20; $Attempt++) {
    Start-Sleep -Milliseconds 500
    try {
        $Health = Invoke-RestMethod -Uri 'http://127.0.0.1:6543/api/v1/health' -TimeoutSec 2
        if ($Health.status -eq 'ok') {
            $Healthy = $true
            break
        }
    }
    catch {
        # The process may still be starting.
    }
}

if (-not $Healthy) {
    throw "The scheduled task was registered, but the health check failed. Inspect $ProjectRoot\log\server-monitor.log."
}

Write-Host 'Server Monitor is running in the background and will start when this user signs in.'
Write-Host 'Health endpoint: http://127.0.0.1:6543/api/v1/health'
