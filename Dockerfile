FROM python:3.8-slim

EXPOSE 8080

RUN apt-get update && apt-get install -y -qq wget gnupg2 unzip


WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN flask db upgrade

CMD [ "gunicorn", "--log-level=INFO", "--bind", "0.0.0.0:8080", "wsgi:app" ]

