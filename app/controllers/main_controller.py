from flask import render_template, request
from app.controllers.base_controller import BaseController
import requests


class MainController(BaseController):
    def index():
        return render_template('resources/views/admin/base/index.html')