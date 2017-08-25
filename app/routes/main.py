from flask import Blueprint, render_template
from app.controllers.main_controller import MainController


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return MainController.index()

@main.route('/attendees')
def getAttendees():
    return MainController.getAttendees()

@main.route('/payments')
def getPayments():
    return MainController.getPayments()

@main.route('/login')
def login():
    return render_template('admin/auth/login.html')
