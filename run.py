#!/usr/bin/env python3
"""
Teccam SGT Application Runner.
Starts the web service on port 8600 using Gunicorn (production WSGI) or Flask dev server.
"""
import sys
import os
import subprocess
from pathlib import Path

def main():
    root = Path(__file__).resolve().parent
    port = os.getenv("PORT", "8600")
    host = os.getenv("HOST", "0.0.0.0")
    workers = os.getenv("WORKERS", "2")

    # If --dev flag is passed, run with Flask directly
    if "--dev" in sys.argv:
        print(f"[*] Starting Teccam SGT (Development Mode) on http://{host}:{port} ...")
        from app import create_app
        app = create_app()
        app.run(host=host, port=int(port), debug=True)
        return

    # Default: Run with Gunicorn WSGI server
    gunicorn_bin = root / "venv" / "bin" / "gunicorn"
    if not gunicorn_bin.exists():
        gunicorn_bin = "gunicorn"

    cmd = [
        str(gunicorn_bin),
        "--bind", f"{host}:{port}",
        "--workers", str(workers),
        "--access-logfile", "-",
        "--error-logfile", "-",
        "wsgi:app"
    ]

    print(f"[*] Starting Teccam SGT with Gunicorn on http://{host}:{port} ({workers} workers) ...")
    sys.exit(subprocess.call(cmd))

if __name__ == "__main__":
    main()
