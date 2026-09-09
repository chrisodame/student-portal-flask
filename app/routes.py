from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from .models import Student
from .forms import StudentForm
from . import db

import os
from werkzeug.utils import secure_filename
from flask import current_app

main = Blueprint("main", __name__)


@main.route("/")
def home():

    total_students = Student.query.count()

    male_students = Student.query.filter_by(
        gender="Male"
    ).count()

    female_students = Student.query.filter_by(
        gender="Female"
    ).count()

    courses = db.session.query(Student.course).distinct().count()

    recent_students = Student.query.order_by(
        Student.created_at.desc()
    ).limit(5).all()

    return render_template(
        "dashboard.html",
        total_students=total_students,
        male_students=male_students,
        female_students=female_students,
        courses=courses,
        recent_students=recent_students,
    )

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

@main.route("/students/<int:id>/id-card")
def student_id_card(id):

    student = Student.query.get_or_404(id)

    return render_template(
        "student_id_card.html",
        student=student
    )

@main.route("/students/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)

    if form.validate_on_submit():

        student.student_number = form.student_number.data
        student.first_name = form.first_name.data
        student.last_name = form.last_name.data
        student.gender = form.gender.data
        student.date_of_birth = form.date_of_birth.data
        student.email = form.email.data
        student.phone = form.phone.data
        student.address = form.address.data
        student.course = form.course.data
        student.level = form.level.data
        student.guardian_name = form.guardian_name.data
        student.guardian_phone = form.guardian_phone.data

        if form.photo.data:

            photo = form.photo.data

            filename = secure_filename(photo.filename)

            upload_folder = os.path.join(
                current_app.static_folder,
                "uploads"
            )

            os.makedirs(upload_folder, exist_ok=True)

            photo.save(os.path.join(upload_folder, filename))

            student.photo = filename

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
        
        filename = None

        if form.photo.data:
            file = form.photo.data
            filename = secure_filename(file.filename)

            file.save(
                os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            filename
                )
            )

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
             
             photo=filename
        )

        db.session.add(student)
        db.session.commit()

        flash("Student registered successfully!", "success")
        return redirect(url_for("main.students"))

    return render_template("add_student.html", form=form)

   