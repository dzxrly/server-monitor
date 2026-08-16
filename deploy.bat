@echo off
setlocal
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0deploy\windows\install.ps1"
if errorlevel 1 exit /b %errorlevel%
