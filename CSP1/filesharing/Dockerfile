FROM python:3.9-alpine

WORKDIR /usr/src/app

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
RUN apk update && apk add python3-dev gcc g++ libc-dev

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt 

COPY app/ ./app
RUN rm -r app/db app/uploads; mkdir app/db app/uploads && chown appuser:appgroup app/db app/uploads

COPY flag.txt app/uploads/ffffffffffffffffffffffffffffffff
RUN chmod -R 777 ./app
ENV EMAIL_FILESHARING=admin@m0lecon.it
ENV PASSWORD_FILESHARING=REDACTED

USER appuser
RUN flask create-db

EXPOSE 8080/tcp

CMD export SECRET_KEY=$(cat /dev/urandom | base64 | head -c 30) && gunicorn -w 4 --bind :8080 "app:create_app()" --user appuser --group appgroup