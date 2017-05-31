import os
from app import create_app
from flask.ext.script import Manager, Shell

print('Before creating application')
application = create_app(os.getenv('FLASK_CONFIG') or 'default')
print('After creating application')

print('Before import app views')
import app.views
app.views.set_app_routes(application)
print('After import app views')

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8086, debug=True)
