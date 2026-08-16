@echo off
setlocal
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0deploy\windows\uninstall.ps1"
if errorlevel 1 exit /b %errorlevel%
