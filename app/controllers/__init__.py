"""Controllers package initialization."""
from .home_controller import home_bp
from .error_controller import error_bp
from .label_controller import label_bp

__all__ = ["home_bp", "error_bp", "label_bp"]
