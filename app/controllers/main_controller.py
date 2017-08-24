from flask import render_template
from app.controllers.base_controller import BaseController


class MainController(BaseController):
    def index():
        return render_template('resources/views/admin/base/index.html')
