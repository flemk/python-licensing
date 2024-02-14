# Use an official Python runtime as a parent image
FROM python:3.9.18-slim-bullseye

# Set environment variables
ENV DB_NAME=your_database
ENV DB_USER=your_username
ENV DB_PASS=your_password
ENV DB_HOST=localhost
ENV DB_PORT=5432

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Generate a self-signed certificate
RUN openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj '/CN=localhost'

# Make port 5000 available to the world outside this container
EXPOSE 5000

# (dev) Run server.py when the container launches
CMD ["python", "server.py"]

# (prod) Run the command to start Gunicorn
#CMD ["gunicorn", "-b", "0.0.0.0:5000", "server:app"]