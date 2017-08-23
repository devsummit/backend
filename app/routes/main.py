from flask import Blueprint, render_template, request


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('resources/views/admin/base/index.html')


@main.route('/login')
def login():
    return render_template('resources/views/admin/auth/login.html')
