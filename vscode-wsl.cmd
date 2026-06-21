@echo off
pushd %~dp0
for /f "delims=" %%a in ('wsl wslpath -u "%CD%"') do (
    wsl bash -ic "cd \"%%a\" && code ."
)
popd
