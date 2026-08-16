FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SERVER_MONITOR_LOG_DIR=/home/server-monitor/.local/state/server-monitor

RUN useradd --create-home --uid 10001 server-monitor
WORKDIR /app

COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY --chown=server-monitor:server-monitor . .
USER server-monitor

EXPOSE 6543
CMD ["python", "server.py"]
