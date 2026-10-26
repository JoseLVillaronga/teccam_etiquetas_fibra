from flask import Blueprint, render_template, current_app
from app.models.ot_model import OtMetricModel

home_bp = Blueprint("home", __name__)

@home_bp.route("/", methods=["GET"], strict_slashes=True)
def index():
    """
    Renders the Home / OT Analysis dashboard replicating Teccam SGT aesthetics.
    Strict route mapping ensures deterministic behavior.
    """
    chart_data = OtMetricModel.get_dashboard_data()
    return render_template(
        "home/index.html",
        active_nav="inicio",
        chart_data=chart_data,
        app_name=current_app.config.get("APP_NAME"),
        company_name=current_app.config.get("COMPANY_NAME"),
        company_email=current_app.config.get("COMPANY_EMAIL"),
        copyright_year=current_app.config.get("COPYRIGHT_YEAR"),
    )
