# Dockerfile
# Using the official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy application files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for the application
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
