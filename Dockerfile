FROM python:3.10

WORKDIR /app

COPY . .

RUN python3.10 -m pip install -r requirements.txt
