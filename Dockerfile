FROM python:3.13.0b1-alpine3.19

WORKDIR /app

COPY app ./app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=app/main.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run"]