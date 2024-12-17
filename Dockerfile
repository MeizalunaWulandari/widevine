# Use the official Python image as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /.

# Copy the application files into the working directory
COPY . /.

# Install the application dependencies
RUN pip install -r requirements.txt

# Set environment variable for Flask app
ENV FLASK_APP=main.py

# Expose port 5000
EXPOSE 5000

# Define the entry point for the container
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
