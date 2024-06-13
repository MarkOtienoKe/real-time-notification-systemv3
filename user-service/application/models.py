from . import db
from flask_login import UserMixin
from datetime import datetime
from passlib.hash import pbkdf2_sha256

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(255), unique=False, nullable=True)
    last_name = db.Column(db.String(255), unique=False, nullable=True)
    password = db.Column(db.String(255), unique=False, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_authenticated = db.Column(db.Boolean, default=False)
    api_key = db.Column(db.String(255), unique=True, nullable=True)
    date_time_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_time_modified = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def encode_api_key(self):
        self.api_key = pbkdf2_sha256.hash(self.username + str(datetime.utcnow))

    def encode_password(self):
        self.password = pbkdf2_sha256.hash(self.password)

    def to_json(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'id': self.id,
            'api_key': self.api_key,
            'is_active': True,
            'is_admin': self.is_admin,
            'is_authenticated': self.is_authenticated,
        }
