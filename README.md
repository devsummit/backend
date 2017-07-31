# Read Me

## setup instruction 

- clone the repo to your local machine
- run `make env` to setup your environments, this will chain to run `make dep` automatically to install all dependencies in `requirements.txt`
- activate the virtual environment by running `source env/bin/activate`
- database migration can be done by the following steps:
	- create a database file by `touch app.db`, naming convention follows the configuration in `alembic.ini` `sqlalchemy.url` value.
	- migrate by run `alembic upgrade head`
- run the server by `python manage.py server`.