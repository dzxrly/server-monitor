from server_monitor.application import create_app
from server_monitor.config import Settings

if __name__ == "__main__":
    settings = Settings.from_env()
    create_app(settings).run(
        host=settings.host,
        port=settings.port,
        debug=True,
        use_reloader=False,
    )
