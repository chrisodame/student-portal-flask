from datetime import datetime
from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(100), nullable=False)

    last_name = db.Column(db.String(100), nullable=False)

    username = db.Column(db.String(80), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), default="student")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    enrollments = db.relationship(
        "Enrollment",
        backref="student",
        lazy=True
    )

    def __repr__(self):
        return f"<User {self.username}>"




class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)

    course_code = db.Column(db.String(20), unique=True, nullable=False)

    course_name = db.Column(db.String(150), nullable=False)

    credit_hours = db.Column(db.Integer)

    lecturer = db.Column(db.String(100))

    enrollments = db.relationship(
        "Enrollment",
        backref="course",
        lazy=True
    )

    def __repr__(self):
        return f"<Course {self.course_code}>"




class Enrollment(db.Model):
    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id")
    )

    semester = db.Column(db.String(50))

    grade = db.relationship(
        "Grade",
        backref="enrollment",
        uselist=False
    )




class Grade(db.Model):
    __tablename__ = "grades"

    id = db.Column(db.Integer, primary_key=True)

    enrollment_id = db.Column(
        db.Integer,
        db.ForeignKey("enrollments.id")
    )

    score = db.Column(db.Float)

    letter_grade = db.Column(db.String(2))

    remarks = db.Column(db.String(100))


from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))