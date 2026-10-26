"""WSGI entrypoint for Gunicorn web server."""
from app import create_app

app = create_app()

if __name__ == "__main__":
    port = app.config.get("PORT", 8600)
    host = app.config.get("HOST", "0.0.0.0")
    debug = app.config.get("DEBUG", False)
    app.run(host=host, port=port, debug=debug)
