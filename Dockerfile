FROM python:3.8.19-slim

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt
