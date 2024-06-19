FROM python:3.9.19-slim

WORKDIR /server

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "server.py"]

EXPOSE 6543
