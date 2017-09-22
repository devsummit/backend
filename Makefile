.PHONY: docs test

help:
	@echo "  env         create a development environment using virtualenv"
	@echo "  deps        install dependencies using pip"

env:
	# sudo pacman -S python-pip
	# sudo pacman -S python-virtualenv 
	sudo apt-get install -y python3.6 python-virtualenv
	virtualenv -p python3.6 env && \
	. env/bin/activate

lint:
	flake8 --config=flake8.ini .

deps:
	pip install -r requirements.txt
