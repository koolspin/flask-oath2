import os
from app import create_app, db
from flask.ext.script import Manager, Shell

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

@manager.command
def create():
    "Creates database tables from sqlalchemy models"
    db.create_all()
    db.session.commit()

# def make_shell_context():
#     return dict(app=app, db=db, User=User, Role=Role)
# manager.add_command("shell", Shell(make_context=make_shell_context))
# manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
