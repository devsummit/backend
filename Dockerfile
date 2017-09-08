FROM python:3.6.2

ADD . /backend
WORKDIR /backend

EXPOSE 5000

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]