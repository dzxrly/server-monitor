$ErrorActionPreference = 'Stop'
Start-ScheduledTask -TaskName 'Server Monitor'
Write-Host 'Server Monitor start requested.'
