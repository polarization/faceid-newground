#! encoding=utf-8
from flask.ext.script import Server, Manager
from newground.app import create_app

app = create_app()
manager = Manager(app)

manager.add_command("runserver", Server('0.0.0.0', port=7070, threaded=True))


if __name__ == "__main__":
    manager.run()
