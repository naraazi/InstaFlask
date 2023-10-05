from app.extensions import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedSerializer as Serializer
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), unique=True, nullable=False)
    is_confirmed = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_serializer_token(self):
        s = Serializer(current_app.secret_key, salt='default')
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_serializer_token(self, token, max_age=600):
        s = Serializer(current_app.secret_key, salt='default')
        try:
            user_id = s.load(token, max_age=max_age) == self.id
        except:
            return None
        return User.query.get(user_id)
