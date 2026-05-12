from flask import Flask


def new_app() -> Flask:
    app = Flask('gatekeeper')
    from config import flask_default
    app.config.from_object(flask_default)

    with app.app_context():
        # TODO поправить, в двух местах один и тот же вызов моделей
        from internal.models import catalog, identity, processing, risk, vault  # noqa
        from internal.util import dbc
        dbc.init_app(app)

    return app
