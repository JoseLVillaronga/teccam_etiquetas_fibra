import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    """Base application configuration."""
    SECRET_KEY = os.getenv("SECRET_KEY", "teccam-sgt-local-dev-key-2026")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8600))
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
    
    # Strict route matching
    # When STRICT_SLASHES is True, Flask will strictly enforce route slashes
    STRICT_SLASHES = True
    
    # App Metadata
    APP_NAME = "Sistema de Gestión Teccam (SGT)"
    COMPANY_NAME = "Teccam S.R.L."
    COMPANY_EMAIL = "info@teccamsrl.com.ar"
    COPYRIGHT_YEAR = "2021"
