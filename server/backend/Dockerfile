# Use an official Python runtime as a parent image
FROM python:3.11.3

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Set environment variable to run Python in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000