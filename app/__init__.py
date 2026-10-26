from pathlib import Path
from flask import Flask
from app.config import Config
from app.controllers.home_controller import home_bp
from app.controllers.error_controller import error_bp
from app.controllers.label_controller import label_bp
from app.models.label_model import LABEL_REGISTRY

def create_app(config_class=Config) -> Flask:
    """
    Application factory for the Teccam SGT web app.
    Enforces strict routing, modular blueprints, and custom error boundaries.
    """
    base_dir = Path(__file__).resolve().parent
    template_dir = base_dir / "templates"
    static_dir = base_dir / "static"

    app = Flask(
        __name__,
        template_folder=str(template_dir),
        static_folder=str(static_dir),
        static_url_path="/static"
    )
    
    app.config.from_object(config_class)
    
    # Enforce strict routing rules globally
    app.url_map.strict_slashes = app.config.get("STRICT_SLASHES", True)
    
    # Context processor to provide global labels list for nav
    @app.context_processor
    def inject_global_data():
        return {
            "all_labels": LABEL_REGISTRY.values()
        }

    # Register blueprints (Controllers)
    app.register_blueprint(home_bp)
    app.register_blueprint(error_bp)
    app.register_blueprint(label_bp)
    
    return app
