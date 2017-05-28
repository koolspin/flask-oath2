import os
from app import create_app
from flask.ext.script import Manager, Shell

application = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8086, debug=True)
