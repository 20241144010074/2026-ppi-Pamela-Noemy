import os

from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        DATABASE=os.path.join(
            app.instance_path,
            "filmes.sqlite"
        )
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import routes
    app.register_blueprint(routes.bp)

    return app