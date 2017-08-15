from flask import request
import datetime


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
