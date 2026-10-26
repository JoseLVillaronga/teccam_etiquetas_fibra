import datetime
from flask import Blueprint, render_template, request, current_app

error_bp = Blueprint("errors", __name__)

@error_bp.app_errorhandler(404)
def handle_not_found(error):
    """
    Custom 404 handler for strict route control.
    Provides unambiguous cognitive clarity (ASD-STE100 standard).
    """
    return render_template(
        "errors/404.html",
        path=request.path,
        method=request.method,
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        company_name=current_app.config.get("COMPANY_NAME", "Teccam S.R.L."),
        company_email=current_app.config.get("COMPANY_EMAIL", "info@teccamsrl.com.ar"),
        copyright_year=current_app.config.get("COPYRIGHT_YEAR", "2021"),
    ), 404

@error_bp.app_errorhandler(500)
def handle_server_error(error):
    """Fallback 500 internal server error handler."""
    return render_template(
        "errors/404.html",
        error_code="500",
        error_title="Error Interno del Servidor",
        error_message="Se produjo un fallo inesperado al procesar la solicitud.",
        path=request.path,
        method=request.method,
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        company_name=current_app.config.get("COMPANY_NAME", "Teccam S.R.L."),
        company_email=current_app.config.get("COMPANY_EMAIL", "info@teccamsrl.com.ar"),
        copyright_year=current_app.config.get("COPYRIGHT_YEAR", "2021"),
    ), 500
