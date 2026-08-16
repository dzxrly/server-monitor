[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$TaskName = 'Server Monitor'
$Task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($Task) {
    Stop-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host 'Server Monitor scheduled task removed. The venv, logs, and sensor runtime were preserved.'
}
else {
    Write-Host 'Server Monitor scheduled task is not installed.'
}
