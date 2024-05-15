FROM python:3.9.18-slim-bullseye

ENV LICENSE_PORT=5000
ENV LICENSE_PORT_EXTERNAL=5001
EXPOSE $LICENSE_PORT_EXTERNAL

WORKDIR /app
ADD . /app
RUN pip install --no-cache-dir -r requirements.txt

RUN openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj '/CN=localhost'
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*
RUN sed -i "s/%LICENSE_PORT_EXTERNAL%/${LICENSE_PORT_EXTERNAL}/g" nginx.conf
RUN sed -i "s/%LICENSE_PORT%/${LICENSE_PORT}/g" nginx.conf
COPY nginx.conf /etc/nginx/sites-available/default

# DEV: CMD ["python", "server.py"]

# PROD:
CMD nginx -c /app/nginx.conf && python server.py
