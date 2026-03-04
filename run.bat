@echo off

:: TODO: Change the path below to your own project directory
cd /d "C:\YOUR\PATH\TO\PROJECT"

echo Starting Ollama...
start /b cmd /c "ollama serve >nul 2>&1"

echo Waiting for Ollama to start...
timeout /t 5 /nobreak >nul

echo Starting Translator Bot...
python cli.py
