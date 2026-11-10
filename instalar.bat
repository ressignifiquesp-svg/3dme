@echo off
setlocal
cd /d "%~dp0"
title Instalador 3DME - Idol Studio
echo ==========================================
echo       3DME - INSTALACAO WINDOWS
echo ==========================================
where py >nul 2>nul
if errorlevel 1 (
  echo Python nao encontrado. Instale Python 3.11 x64 em https://www.python.org/downloads/
  echo Marque Add Python to PATH durante a instalacao.
  pause
  exit /b 1
)
where git >nul 2>nul
if errorlevel 1 (
  echo Git nao encontrado. Instale Git for Windows em https://git-scm.com/download/win
  pause
  exit /b 1
)
if not exist "vendor\idol-sdk\pyproject.toml" (
  if not exist "vendor" mkdir vendor
  echo Baixando o Idol SDK oficial...
  git clone https://github.com/speridlabs/idol-sdk.git vendor\idol-sdk
  if errorlevel 1 (
    echo Falha ao baixar o SDK.
    pause
    exit /b 1
  )
)
if not exist ".venv\Scripts\python.exe" (
  py -3.11 -m venv .venv
  if errorlevel 1 (
    echo Nao foi possivel criar ambiente Python 3.11.
    pause
    exit /b 1
  )
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
echo Instalando PyTorch CUDA 12.4...
python -m pip install torch==2.6.0 torchvision==0.21.0 --index-url https://download.pytorch.org/whl/cu124
if errorlevel 1 (
  echo Falha ao instalar PyTorch CUDA.
  pause
  exit /b 1
)
echo Instalando Idol SDK e Gradio...
cd vendor\idol-sdk
python -m pip install -e ".[demo]"
if errorlevel 1 (
  echo Falha ao instalar Idol SDK.
  pause
  exit /b 1
)
cd ..\..
echo.
echo Instalacao concluida. Configure o Hugging Face conforme README.md.
pause
