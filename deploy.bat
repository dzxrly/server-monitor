echo "Creating virtual environment: ./env"
python -m venv ./env
echo "Activating virtual environment: ./env & Installing requirements && Deploying..."
.\env\Scripts\activate.bat && pip install -r requirements.txt && python server.py
