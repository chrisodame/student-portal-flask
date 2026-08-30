from flask import Blueprint, render_template, redirect, url_for, flash
from .models import Student
from .forms import StudentForm
from . import db

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("index.html")


@main.route("/students")
def students():
    student_list = Student.query.order_by(Student.created_at.desc()).all()
    return render_template("students.html", students=student_list)


@main.route("/students/add", methods=["GET", "POST"])
def add_student():
    form = StudentForm()

    if form.validate_on_submit():

        existing_student = Student.query.filter(
            (Student.student_number == form.student_number.data)
            | (Student.email == form.email.data)
        ).first()

        if existing_student:
            flash("Student Number or Email already exists.", "danger")
            return redirect(url_for("main.add_student"))

        student = Student(
            student_number=form.student_number.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            gender=form.gender.data,
            date_of_birth=form.date_of_birth.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            course=form.course.data,
            level=form.level.data,
            guardian_name=form.guardian_name.data,
            guardian_phone=form.guardian_phone.data,
        )

        db.session.add(student)
        db.session.commit()

        flash("Student registered successfully!", "success")
        return redirect(url_for("main.students"))

    return render_template("add_student.html", form=form)