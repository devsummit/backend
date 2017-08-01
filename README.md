# Read Me

## setup instruction 

- clone the repo to your local machine
- run `make env` to setup your environments.
- activate the virtual environment by running `source env/bin/activate`
- run `make deps` inside `env` to automatically install all dependencies in `requirements.txt`
- database migration can be done by the following steps:
	- create a database file by `touch app.db`, naming convention follows the configuration in `alembic.ini` `sqlalchemy.url` value.
	- migrate by run `alembic upgrade head`
- run the server by `python manage.py server`.

# Linting

Make sure flake-8 is installed on your env, by running `make deps` inside your `env`

Linting is achieved by integrating [flake8](http://flake8.pycqa.org). <br>
You can check you PEP8 compliance by typing: `make lint`
