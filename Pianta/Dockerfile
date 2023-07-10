FROM python:3.11.0-alpine3.15

ENV PYTHONUNBUFFERED=1

WORKDIR /Pianta

COPY ./requirements.txt ./

RUN apk add --no-cache mariadb-connector-c-dev build-base \
    && pip install -r requirements.txt \
    && apk del build-base

COPY ./ ./ ./ ./

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
