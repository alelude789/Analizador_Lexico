from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'automatas-lexer-2026'
    app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB max upload

    # Register blueprints (controllers)
    from app.controllers.lexer_controller import lexer_bp
    app.register_blueprint(lexer_bp)

    return app