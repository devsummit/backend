FROM python:3.6.2

ADD . /backend
WORKDIR /backend

# install needed tools
RUN apt-get update
RUN apt-get install -y sqlite3 libsqlite3-dev

EXPOSE 5000

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]