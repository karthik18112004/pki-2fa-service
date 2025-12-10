FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY cron ./cron
COPY keys ./keys

RUN ["chmod", "+x", "/app/cron/cronjob.sh"]

EXPOSE 8080

CMD sh -c "/app/cron/cronjob.sh & uvicorn app.main:app --host 0.0.0.0 --port 8080"
