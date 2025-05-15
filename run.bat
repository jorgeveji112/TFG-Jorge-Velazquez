
@echo off
echo Activando entorno virtual...
call .venv\Scripts\activate.bat

echo Estableciendo PYTHONPATH...
set PYTHONPATH=src

echo Lanzando simulación multiagente...
python main.py

pause
