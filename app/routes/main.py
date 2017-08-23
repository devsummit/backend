from flask import Blueprint, render_template, request
from app.controllers.main_controller import MainController


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return MainController.index()

@main.route('/attendees')
def getAttendees():
    return MainController.getAttendees()



@main.route('/login')
def login():
    return render_template('admin/auth/login.html')
