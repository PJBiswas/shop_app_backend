@echo off
echo ===============================
echo Checking for .venv environment ...
echo ===============================

IF NOT EXIST ".venv" (
    echo .venv folder not found. Creating virtual environment ...
    python -m venv .venv
) ELSE (
    echo .venv exists.
)

echo ===============================
echo Activating FastAPI .venv ...
echo ===============================
call .venv\Scripts\activate.bat

echo ===============================
echo Installing requirements ...
echo ===============================
pip install -r requirements.txt

echo ===============================
echo Starting FastAPI server ...
echo ===============================
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

echo ===============================
echo Server stopped.
echo ===============================
pause
