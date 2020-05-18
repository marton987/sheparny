FROM python:3.8

COPY . app/

WORKDIR /app

RUN apt-get update && \
    apt-get -y upgrade
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python manage.py migrate
