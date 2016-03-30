from flask import Flask
import resources

_app = Flask(__name__, template_folder='templates', static_folder='static')


def configure_foundations(app):

    @app.after_request
    def releaseDB(response):
        return response

    @app.before_request
    def before_request():
        pass


def configure_blueprint(app, modules):
    for module in modules:
        app.register_blueprint(module)


def create_app():
    _app.config.from_object('config')
    configure_foundations(_app)
    configure_blueprint(_app, resources.MODULES)

    create_app = lambda: _app
    return create_app()