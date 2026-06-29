from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from .models import User
from .forms import RegistrationForm, LoginForm
from . import db

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("index.html")


@main.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = RegistrationForm()

    if form.validate_on_submit():

        existing_user = User.query.filter(
            (User.email == form.email.data) |
            (User.username == form.username.data)
        ).first()

        if existing_user:
            flash("Email or username already exists.", "danger")
            return redirect(url_for("main.register"))

        hashed_password = generate_password_hash(form.password.data)

        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("main.login"))

    return render_template("register.html", form=form)


@main.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):

            login_user(user)

            flash("Welcome back!", "success")

            return redirect(url_for("main.dashboard"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html", form=form)


@main.route("/dashboard")
@login_required
def dashboard():

    return render_template("dashboard.html")


@main.route("/logout")
@login_required
def logout():

    logout_user()

    flash("You have been logged out.", "info")

    return redirect(url_for("main.home"))