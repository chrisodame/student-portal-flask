from datetime import datetime

from . import db


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_number = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    first_name = db.Column(
        db.String(100),
        nullable=False
    )

    last_name = db.Column(
        db.String(100),
        nullable=False
    )

    gender = db.Column(
        db.String(10),
        nullable=False
    )

    date_of_birth = db.Column(
        db.Date,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    phone = db.Column(
        db.String(20),
        nullable=False
    )

    address = db.Column(
        db.Text,
        nullable=False
    )

    course = db.Column(
        db.String(100),
        nullable=False
    )

    level = db.Column(
        db.String(50),
        nullable=False
    )

    guardian_name = db.Column(
        db.String(100)
    )

    guardian_phone = db.Column(
        db.String(20)
    )

    jamb_score = db.Column(
        db.Integer
    )

    admission_status = db.Column(
        db.String(30),
        nullable=False,
        default="Undecided"
    )

    photo = db.Column(
        db.String(255)
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Student {self.student_number}>"