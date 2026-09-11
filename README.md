# Student Portal

A full-stack Student Management Portal built with Python and Flask.

## Project Overview

The Student Portal is a web-based application designed to help manage
student information in a simple and organized way.

The system allows users to register students, view student records,
edit student information, upload student profile photos and manage
student profiles.

## Features

- Student registration
- Student profile management
- Student photo upload
- Student records listing
- Student search
- Student details page
- Edit student information
- Delete student records
- Student ID card
- User registration and login
- Protected dashboard
- Responsive Bootstrap interface
- SQLite database
- Database migrations

## Technologies Used

### Backend

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-WTF
- WTForms
- Flask-Login

### Frontend

- HTML5
- CSS3
- Bootstrap 5
- Jinja2

### Database

- SQLite

## Project Structure

```text
student_portal/
│
├── app/
│   ├── templates/
│   ├── __init__.py
│   ├── config.py
│   ├── forms.py
│   ├── models.py
│   └── routes.py
│
├── instance/
├── migrations/
├── .gitignore
├── requirements.txt
├── run.py
└── README.md