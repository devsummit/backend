# Read Me

## setup instruction 

- clone the repo to your local machine
- copy the `.env.example` if you need to run on local machine `cp .env.example .env` and change the value accordingly.
- create database called `devsummit` on your mysql if you haven't  change the `DB_NAME` on `.env` file.
- run `make env` to setup your environments.
- activate the virtual environment by running `source env/bin/activate`
- run `make deps` inside `env` to automatically install all dependencies in `requirements.txt`
- database migration can be done by the following steps:
	- create a database file by `touch app.db`, naming convention follows the configuration in `alembic.ini` `sqlalchemy.url` value.
	- migrate by run `alembic upgrade head`
- seed the table by running:
	`python manage.py seed`
- run the server by `python manage.py server`.

## Run On Docker

You can run the server on docker simply by running:
*not in virtual environment

- `docker-compose build`
- `docker-compose up` 
- `docker-compose exec database sh` and run `mysql_upgrade -u root -p`
- `docker-compose exec web sh` and run `alembic upgrade head` then seed by running `python manage.py seed` 

additional setup including `migrations` and `seeding` will be the same as setup instruction above by `docker-compose exec bash web sh` to get into the container environment.
and server should be up on `localhost:5000`

## Linting

Make sure flake-8 is installed on your env, by running `make deps` inside your `env`

Linting is achieved by integrating [flake8](http://flake8.pycqa.org). <br>
You can check you PEP8 compliance by typing: `make lint`

## Api Blueprint

We use hercule to compile the blueprints into single **apib** file.
All the blueprints resided in ```/blueprint``` folder, the main file is blueprint.apib
We also define the datastructure for all blueprint in sepearate apib files, resided in folder ```/blueprint/data```. To compile the blueprint these all what we need tobe done:

- Install hercule first

```sh
	$ npm install -g hercule
```

- Compile
```
	$ hercule blueprint/blueprint.apib -o apiary.apib
```

## Api Testing

-  To run the apiary test we need ```dredd cli``` installed globally

```sh
	$ npm install -g dredd
```

- Then run the test in the project root folder

```sh
	$ dredd
```

