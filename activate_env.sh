#!/bin/bash

echo "==============================="
echo "Checking for .venv environment ..."
echo "==============================="

if [ ! -d ".venv" ]; then
  echo ".venv folder not found. Creating virtual environment ..."
  python3 -m venv .venv
else
  echo ".venv exists."
fi

echo "==============================="
echo "Activating FastAPI .venv ..."
echo "==============================="
source .venv/bin/activate

echo "==============================="
echo "Installing requirements ..."
echo "==============================="
pip install -r requirements.txt

echo "==============================="
echo "Starting FastAPI server ..."
echo "==============================="
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

echo "==============================="
echo "Server stopped."
echo "==============================="
