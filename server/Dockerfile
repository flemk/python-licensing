FROM python:3.9.18-slim-bullseye

ARG DB_NAME
ENV DB_NAME=$DB_NAME
ARG DB_USER
ENV DB_USER=$DB_USER
ARG DB_PASS
ENV DB_PASS=$DB_PASS
ARG DB_HOST
ENV DB_HOST=$DB_HOST
ARG DB_PORT
ENV DB_PORT=$DB_PORT

ARG ENVIRONMENT
ENV ENVIRONMENT=$ENVIRONMENT

ARG LICENSE_PORT
ENV LICENSE_PORT=$LICENSE_PORT

ARG LICENSE_PORT_EXTERNAL
ENV LICENSE_PORT_EXTERNAL=$LICENSE_PORT_EXTERNAL
EXPOSE $LICENSE_PORT_EXTERNAL

WORKDIR /app
ADD . /app
RUN pip install --no-cache-dir -r requirements.txt

RUN openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj '/CN=localhost'
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*
COPY nginx.conf /etc/nginx/sites-available/default
RUN sed -i "s/%LICENSE_PORT_EXTERNAL%/${LICENSE_PORT_EXTERNAL}/g" /etc/nginx/sites-available/default
RUN sed -i "s/%LICENSE_PORT%/${LICENSE_PORT}/g" /etc/nginx/sites-available/default

# DEV: CMD ["python", "server.py"]

# PROD:
CMD service nginx start && python server.py
