from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from .models import Student
from .forms import StudentForm
from . import db

import os
from werkzeug.utils import secure_filename
from flask import current_app

main = Blueprint("main", __name__)


courses_by_level = {
    "100": [
        "Computer Science",
        "Software Engineering",
        "Information Technology",
        "Cyber Security"
    ],
    "200": [
        "Computer Science",
        "Software Engineering",
        "Information Technology",
        "Cyber Security"
    ],
    "300": [
        "Computer Science",
        "Software Engineering",
        "Information Technology",
        "Cyber Security"
    ],
    "400": [
        "Computer Science",
        "Software Engineering",
        "Information Technology",
        "Cyber Security"
    ]
}

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

@main.route("/about")
def about():
    return render_template("about.html")

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

@main.route("/api/courses/<level>")
def get_courses(level):

    courses_by_level = {
        "100": [
            "Computer Science",
            "Information Technology",
            "Software Engineering",
            "Cybersecurity"
        ],
        "200": [
            "Computer Science",
            "Information Technology",
            "Software Engineering",
            "Cybersecurity"
        ],
        "300": [
            "Computer Science",
            "Information Technology",
            "Software Engineering",
            "Cybersecurity"
        ],
        "400": [
            "Computer Science",
            "Information Technology",
            "Software Engineering",
            "Cybersecurity"
        ]
    }

    courses = courses_by_level.get(level, [])

    return {
        "courses": courses
    }

@main.route("/students/<int:id>/admission-status", methods=["POST"])
def update_admission_status(id):
    student = Student.query.get_or_404(id)

    admission_status = request.form.get("admission_status")

    allowed_statuses = [
        "Undecided",
        "Admitted",
        "Not Admitted"
    ]

    if admission_status not in allowed_statuses:
        flash("Invalid admission status.", "danger")
        return redirect(url_for("main.student_details", id=id))

    student.admission_status = admission_status

    db.session.commit()

    flash("Admission status updated successfully!", "success")

    return redirect(url_for("main.student_details", id=id))

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

    form = StudentForm()

    courses_by_level = {
        "100": [
            "Computer Science",
            "Software Engineering",
            "Information Technology"
        ],
        "200": [
            "Computer Science",
            "Software Engineering",
            "Information Technology"
        ],
        "300": [
            "Computer Science",
            "Software Engineering",
            "Information Technology"
        ],
        "400": [
            "Computer Science",
            "Software Engineering",
            "Information Technology"
        ]
    }

    # -----------------------------------
    # LOAD EXISTING STUDENT DATA
    # -----------------------------------

    if request.method == "GET":

        form.student_number.data = student.student_number
        form.first_name.data = student.first_name
        form.last_name.data = student.last_name
        form.gender.data = student.gender
        form.date_of_birth.data = student.date_of_birth
        form.email.data = student.email
        form.phone.data = student.phone
        form.address.data = student.address
        form.level.data = student.level
        form.course.data = student.course
        form.guardian_name.data = student.guardian_name
        form.guardian_phone.data = student.guardian_phone
        form.jamb_score.data = student.jamb_score
        form.admission_status.data = student.admission_status

    # -----------------------------------
    # SET COURSE OPTIONS
    # -----------------------------------

    selected_level = form.level.data

    course_choices = courses_by_level.get(
        selected_level,
        []
    ).copy()

    # Keep the student's existing course
    # even if it is not currently in the list.
    if student.course and student.course not in course_choices:
        course_choices.append(student.course)

    form.course.choices = [
        (course, course)
        for course in course_choices
    ]

    # -----------------------------------
    # PROCESS FORM SUBMISSION
    # -----------------------------------

    if form.validate_on_submit():

        existing_student = Student.query.filter(
            (
                Student.student_number == form.student_number.data
            )
            |
            (
                Student.email == form.email.data
            )
        ).filter(
            Student.id != student.id
        ).first()

        if existing_student:

            flash(
                "Student Number or Email already exists.",
                "danger"
            )

            return redirect(
                url_for(
                    "main.edit_student",
                    id=student.id
                )
            )

        # -----------------------------------
        # UPDATE STUDENT INFORMATION
        # -----------------------------------

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
        student.jamb_score = form.jamb_score.data
        student.admission_status = form.admission_status.data

        # -----------------------------------
        # UPDATE PHOTO ONLY IF NEW PHOTO
        # IS ACTUALLY UPLOADED
        # -----------------------------------

        if form.photo.data and hasattr(
            form.photo.data,
            "filename"
        ):

            photo = form.photo.data

            filename = secure_filename(
                photo.filename
            )

            upload_folder = os.path.join(
                current_app.static_folder,
                "uploads"
            )

            os.makedirs(
                upload_folder,
                exist_ok=True
            )

            photo.save(
                os.path.join(
                    upload_folder,
                    filename
                )
            )

            student.photo = filename

        # -----------------------------------
        # SAVE CHANGES
        # -----------------------------------

        db.session.commit()

        flash(
            "Student updated successfully!",
            "success"
        )

        return redirect(
            url_for(
                "main.student_details",
                id=student.id
            )
        )

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

    courses_by_level = {
        "100": [
            "Computer Science",
            "Information Technology",
            "Software Engineering",
            "Cybersecurity"
        ],
        "200": [
            "Computer Science",
            "Information Technology",
            "Software Engineering",
            "Cybersecurity"
        ],
        "300": [
            "Computer Science",
            "Information Technology",
            "Software Engineering",
            "Cybersecurity"
        ],
        "400": [
            "Computer Science",
            "Information Technology",
            "Software Engineering",
            "Cybersecurity"
        ]
    }

    if request.method == "POST":
        form.course.choices = [
            (course, course)
            for course in courses_by_level.get(form.level.data, [])
        ]

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
            jamb_score=form.jamb_score.data,
            admission_status=form.admission_status.data,
            photo=filename
        )

        db.session.add(student)
        db.session.commit()

        flash("Student registered successfully!", "success")
        return redirect(url_for("main.students"))

    return render_template("add_student.html", form=form)