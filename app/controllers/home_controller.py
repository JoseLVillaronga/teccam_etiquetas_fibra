from flask import Blueprint, render_template, current_app, send_from_directory

home_bp = Blueprint("home", __name__)

@home_bp.route("/favicon.ico", methods=["GET"], strict_slashes=True)
def favicon():
    """Serves the label favicon icon file."""
    return send_from_directory(
        current_app.static_folder,
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon"
    )

@home_bp.route("/", methods=["GET"], strict_slashes=True)
def index():
    """
    Renders the Home view with label generation modules.
    Strict route mapping ensures deterministic behavior.
    """
    return render_template(
        "home/index.html",
        active_nav="inicio",
        app_name=current_app.config.get("APP_NAME"),
        company_name=current_app.config.get("COMPANY_NAME"),
        company_email=current_app.config.get("COMPANY_EMAIL"),
        copyright_year=current_app.config.get("COPYRIGHT_YEAR"),
    )
