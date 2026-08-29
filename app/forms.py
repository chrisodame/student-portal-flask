from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from wtforms import (
    StringField,
    SelectField,
    DateField,
    TextAreaField,
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

    gender = SelectField(
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

    course = StringField(
        "Course",
        validators=[DataRequired()]
    )

    level = SelectField(
        "Level",
        choices=[
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

    photo = FileField(
        "Student Photo",
        validators=[
            FileAllowed(["jpg", "jpeg", "png"], "Images only!")
        ]
    )

    submit = SubmitField("Register Student")