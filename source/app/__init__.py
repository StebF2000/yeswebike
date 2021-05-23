from flask import Flask


def init_app():
    app = Flask(__name__, instance_relative_config=False)

    with app.app_context():
        from . import routes

        from .visualizations.bicing_map import bare_map
        from .visualizations.centrality_map import centrality_map

        app = bare_map(app)
        app = centrality_map(app)

    return app
