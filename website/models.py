from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    problems = db.relationship('ProblemInstance')

class ProblemInstance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    problem_id = db.Column(db.Integer, db.ForeignKey('problem.id'))
    problem_name = db.Column(db.String(150))
    correct = db.Column(db.Boolean)
    date = db.Column(db.DateTime(timezone=True), default=func.now())


class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problem_name = db.Column(db.String(100), )
    tags = db.Column(db.String(100))
    difficulty = db.Column(db.Integer)
    description = db.Column(db.String(6000))
    code = db.Column(db.String(7000))
    