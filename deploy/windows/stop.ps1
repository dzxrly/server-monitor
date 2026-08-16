$ErrorActionPreference = 'Stop'
Stop-ScheduledTask -TaskName 'Server Monitor'
Write-Host 'Server Monitor stopped.'
