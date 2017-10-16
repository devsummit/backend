from flask import request, current_app, url_for, jsonify
import datetime
import os


class Helper():
    # Document URL helper, turn into domain based url
    @staticmethod
    def url_helper(url, config):
        return request.url_root + config + url

    # For a given file, retun whether it's an allowed type or not
    @staticmethod
    def allowed_file(file_name, config):
        return '.' in file_name and \
            file_name.rsplit('.', 1)[1] in config

    # Timestamp string maker
    @staticmethod
    def time_string():
        now = datetime.datetime.now()
        return str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + str(now.microsecond)

    # silent remove file that may or may not exist
    @staticmethod
    def silent_remove(filename):
        try:
            os.remove(filename)
        except OSError:
            pass

    @staticmethod
    def __has_no_empty_params(rule):
        defaults = rule.defaults if rule.defaults is not None else ()
        arguments = rule.arguments if rule.arguments is not None else ()
        return len(defaults) >= len(arguments)

    @staticmethod
    def site_map():
        links = []
        for rule in current_app.url_map.iter_rules():
            # Filter out rules we can't navigate to in a browser
            # and rules that require parameters
            if "GET" in rule.methods and Helper.__has_no_empty_params(rule):
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                links.append({rule.endpoint: url, 'role_access': 'admin'})
        return links
