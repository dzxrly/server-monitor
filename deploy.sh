#!/bin/bash

echo "Creating virtual environment: ./env"
python -m venv ./env
echo "Activating virtual environment: ./env"
source env/bin/activate
echo "Installing requirements"
pip install -r requirements.txt
echo "Running server"
python server.py
