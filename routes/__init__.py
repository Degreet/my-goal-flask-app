from .home import home_bp
from .login import login_bp
from .dashboard import dashboard_bp


def setup_routes(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(dashboard_bp)
