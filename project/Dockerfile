# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the application files into the container
COPY ./app /usr/src/app

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 10000
# The default value of PORT is 10000 for all Render web services
EXPOSE 10000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000", "--reload"]
