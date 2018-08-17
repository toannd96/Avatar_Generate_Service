from hashlib import md5
from app import db


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    email_md5 = db.Column(db.String(100))
    picture = db.relationship('Picture', back_populates='users')

    def set_email(self, email):
        self.email_md5 = md5(email.encode('utf-8')).hexdigest()


class Picture(db.Model):

    __tablename__ = 'pictures'

    id = db.Column(db.Integer, primary_key=True)
    name_picture = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship('User', back_populates='picture')
