"""
Quart application entry point
"""

from quart import Quart

from .middleware import install as install_middleware
from .routes import bp, root_bp


def create_app() -> Quart:
    app = Quart(__name__)

    install_middleware(app)
    app.register_blueprint(root_bp)
    app.register_blueprint(bp)

    return app
