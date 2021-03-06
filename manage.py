import os
from flask.ext.script import Manager, Shell
from app import create_app

# load config file of OS.ENVIRONMENT
config_name = os.getenv('FLASK_CONFIG') or 'production'

app = create_app(config_name)
manager = Manager(app)


def make_shell_context():
    return dict(app=app)

manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
