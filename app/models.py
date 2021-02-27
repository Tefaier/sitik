from app import db, login
from flask_login import UserMixin
import datetime


@login.user_loader
def load_user(id):
    return School.query.get(int(id))


class School(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    groups = db.relationship('Group', backref='school', lazy='dynamic')

    def __repr__(self):
        return '<School {}>'.format(self.name)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    students = db.relationship('Student', backref='group', lazy='dynamic')
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))

    def __repr__(self):
        return '<Group {}>'.format(self.name)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    metrics = db.relationship('Metric', backref='student', lazy='dynamic')

    def __repr__(self):
        return '<Student {}>'.format(self.name)


class Metric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.TIMESTAMP, index=True, default=datetime.datetime.utcnow, nullable=False)
    value = db.Column(db.Numeric, index=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __repr__(self):
        return '<Metric {}>'.format(self.value)
