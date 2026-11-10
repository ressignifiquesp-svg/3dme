@echo off
setlocal
cd /d "%~dp0"
title 3DME - Idol Studio
if not exist ".venv\Scripts\activate.bat" (
  echo Projeto ainda nao instalado. Execute instalar.bat primeiro.
  pause
  exit /b 1
)
call .venv\Scripts\activate.bat
set PYTHONPATH=%CD%\vendor\idol-sdk;%PYTHONPATH%
set ATTN_BACKEND=sdpa
python app.py
if errorlevel 1 (
  echo O aplicativo foi encerrado com erro.
  pause
)
