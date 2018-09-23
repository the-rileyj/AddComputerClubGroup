FROM python:3.7.0-alpine3.8

WORKDIR /app

ADD requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

ADD AutoGrouper.py .

ENTRYPOINT ["python", "AutoGrouper.py"]