@echo on>out.txt
@echo off
setlocal enabledelayedexpansion
set "parentfolder=%CD%"
for /r . %%g in (*.*) do (
  set "var=%%g"
  set var=!var:%parentfolder%=!
  echo !var! >> negative.txt
)