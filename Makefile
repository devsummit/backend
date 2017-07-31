.PHONY: docs test

help:
	@echo "  env         create a development environment using virtualenv"
	@echo "  deps        install dependencies using pip"

env:
	# sudo pacman -S python-pip
	# sudo pacman -S python-virtualenv 
	sudo apt-get install -y python3 python-virtualenv
	virtualenv env && \
	. env/bin/activate && \
	make deps

deps:
	pip3 install -r requirements.txt
