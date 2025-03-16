# Use an official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install Flask and Gunicorn
RUN pip install Flask gunicorn

# Copy the application files into the container
COPY . .

RUN pip install -r requirements.txt

# Expose the port the app will run on
EXPOSE 5000

# Command to run the app with Gunicorn (4 workers as an example)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
