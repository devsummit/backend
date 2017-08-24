from flask import Blueprint, render_template
from app.controllers.main_controller import MainController


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return MainController.index()


@main.route('/login')
def login():
    return render_template('resources/views/admin/auth/login.html')
