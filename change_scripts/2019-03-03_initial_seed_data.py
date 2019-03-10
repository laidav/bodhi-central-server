import os
import sys

sys.path.append('..')

from config import config
from flask import Flask
from app.database import User, Role, Dukkha, Subject, Teaching
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(config[os.getenv("FLASK_CONFIG") or "default"])

db = SQLAlchemy()

db.init_app(app)

if __name__ == "__main__":
    with app.app_context():
        user = User.query.first()
        print(user.username)
