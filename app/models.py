from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pkg_resources import require
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


db = SQLAlchemy()


# class Role(db.Model):
#     pass

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    create_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    @property
    def password(self):
        raise AttributeError('password 不是一个可读的属性！')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration = 3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration) 
        return s.dumps({'id': self.id})   

    @staticmethod
    def check_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None    
        return User.query.get(data['id'])


    def __repr__(self):
        return '<User %r>' % self.name

