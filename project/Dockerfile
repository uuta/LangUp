# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src

# Copy the application files into the container
COPY ./app /usr/src

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8400
EXPOSE 8400

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8400", "--reload"]
