@echo off
echo Activando entorno virtual...
call .venv\Scripts\activate.bat

echo Estableciendo PYTHONPATH...
set PYTHONPATH=src

python run_scenarios.py

pause
