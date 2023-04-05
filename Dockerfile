# Use the official Python base image
FROM python:3

# Set the working directory
WORKDIR /code

# Copy requirements.txt and install the required packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .
