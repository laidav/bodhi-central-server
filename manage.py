import os

from app import create_app, db
from app.db_models import User, Role, Post, Subject, PostSubject, Practice, PracticeSubject
from app.modules.BCTree import BCTree
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand, upgrade

app = create_app(os.getenv("FLASK_CONFIG") or "default")
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post,
                Subject=Subject, PostSubject=PostSubject, Practice=Practice,
                PracticeSubject=PracticeSubject, BCTree=BCTree)


@manager.command
def deploy():
    upgrade()


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
