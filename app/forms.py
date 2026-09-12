from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from wtforms import (
    StringField,
    SelectField,
    RadioField,
    DateField,
    TextAreaField,
    IntegerField,
    SubmitField
)

from wtforms.validators import DataRequired, Email


class StudentForm(FlaskForm):
    student_number = StringField(
        "Student Number",
        validators=[DataRequired()]
    )

    first_name = StringField(
        "First Name",
        validators=[DataRequired()]
    )

    last_name = StringField(
        "Last Name",
        validators=[DataRequired()]
    )

    gender = RadioField(
    "Gender",
    choices=[
        ("Male", "Male"),
        ("Female", "Female")
    ],
    validators=[DataRequired()]
    )

    date_of_birth = DateField(
        "Date of Birth",
        format="%Y-%m-%d",
        validators=[DataRequired()]
    )

    email = StringField(
        "Email Address",
        validators=[DataRequired(), Email()]
    )

    phone = StringField(
        "Phone Number",
        validators=[DataRequired()]
    )

    address = TextAreaField(
        "Address",
        validators=[DataRequired()]
    )

    course = SelectField(
        "Course",
        choices=[],
        validators=[DataRequired()]
    )

    level = SelectField(
        "Level",
        choices=[
            ("","Select Level"),
            ("100", "100"),
            ("200", "200"),
            ("300", "300"),
            ("400", "400")
        ],
        validators=[DataRequired()]
    )

    guardian_name = StringField(
        "Guardian Name",
        validators=[DataRequired()]
    )

    guardian_phone = StringField(
        "Guardian Phone",
        validators=[DataRequired()]
    )

    jamb_score = IntegerField(
    "JAMB Score",
    validators=[DataRequired()]
    )

    admission_status = SelectField(
    "Admission Status",
    choices=[
        ("Undecided", "Undecided"),
        ("Admitted", "Admitted"),
        ("Not Admitted", "Not Admitted")
    ],
    validators=[DataRequired()]
    )

    photo = FileField(
        "Student Photo",
        validators=[
            FileAllowed(["jpg", "jpeg", "png"], "Images only!")
        ]
    )

    submit = SubmitField("Register Student")