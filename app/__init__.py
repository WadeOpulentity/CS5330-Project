from flask import Flask, render_template
from .db import get_db

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    # Import and register blueprints for each module
    from .modules.data_entry.routes import data_entry_bp
    from .modules.spaceport_queries.routes import spaceport_queries_bp
    from .modules.route_queries.routes import route_queries_bp
    from .modules.flight_finder.routes import flight_finder_bp

    app.register_blueprint(data_entry_bp, url_prefix='/data_entry')
    app.register_blueprint(spaceport_queries_bp, url_prefix='/spaceport_queries')
    app.register_blueprint(route_queries_bp, url_prefix='/route_queries')
    app.register_blueprint(flight_finder_bp, url_prefix='/flight_finder')

    return app
