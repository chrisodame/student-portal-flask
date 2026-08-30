from flask import Blueprint, render_template, redirect, url_for, flash, request
from .models import Student
from .forms import StudentForm
from . import db

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("index.html")


@main.route("/students")
def students():
    search = request.args.get("search", "").strip()

    query = Student.query

    if search:
        search_pattern = f"%{search}%"

        query = query.filter(
            (Student.student_number.ilike(search_pattern))
            | (Student.first_name.ilike(search_pattern))
            | (Student.last_name.ilike(search_pattern))
            | (Student.email.ilike(search_pattern))
        )

    student_list = query.order_by(
        Student.created_at.desc()
    ).all()

    return render_template(
        "students.html",
        students=student_list,
        search=search
    )

@main.route("/students/<int:id>")
def student_details(id):
    student = Student.query.get_or_404(id)
    return render_template("student_details.html", student=student)

@main.route("/students/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)

    if form.validate_on_submit():
        form.populate_obj(student)

        db.session.commit()

        flash("Student updated successfully!", "success")
        return redirect(url_for("main.students"))

    return render_template(
        "edit_student.html",
        form=form,
        student=student
    )

@main.route("/students/delete/<int:id>", methods=["POST"])
def delete_student(id):
    student = Student.query.get_or_404(id)

    db.session.delete(student)
    db.session.commit()

    flash("Student deleted successfully!", "success")
    return redirect(url_for("main.students"))    

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