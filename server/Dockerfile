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
ARG LICENSE_PORT
ENV LICENSE_PORT=$LICENSE_PORT
EXPOSE $LICENSE_PORT

WORKDIR /app
ADD . /app
RUN pip install --no-cache-dir -r requirements.txt

RUN openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj '/CN=localhost'

# (dev) Run server.py when the container launches
CMD ["python", "server.py"]

# (prod) Run the command to start Gunicorn
#CMD ["gunicorn", "-b", "0.0.0.0:5000", "server:app"]