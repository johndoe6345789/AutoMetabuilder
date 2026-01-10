"""Flask-based API surface that replaces the legacy FastAPI frontend."""
from __future__ import annotations

from flask import Flask

from .routes.context import context_bp
from .routes.navigation import navigation_bp
from .routes.prompt import prompt_bp
from .routes.run import run_bp
from .routes.settings import settings_bp
from .routes.translations import translations_bp

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

app.register_blueprint(context_bp)
app.register_blueprint(run_bp)
app.register_blueprint(prompt_bp)
app.register_blueprint(settings_bp)
app.register_blueprint(translations_bp)
app.register_blueprint(navigation_bp)


def start_web_ui(host: str = "0.0.0.0", port: int = 8000) -> None:
    app.run(host=host, port=port)
