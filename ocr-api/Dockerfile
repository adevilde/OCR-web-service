# Use Ubuntu 20.04 as the base image
FROM ubuntu:20.04

# Set the work directory
WORKDIR /app/ocr-api

# Install Tesseract
RUN apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-eng

# Copy the Python scripts into the container
COPY . /app/ocr-api

# Avoiding user interaction with tzdata
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and pip
RUN apt-get update && apt-get install -y python3.9 python3-pip

# Reset DEBIAN_FRONTEND
ENV DEBIAN_FRONTEND=dialog

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Expose the port the ocr-app runs on
EXPOSE 5000

# Run Uvicorn app when the container launches
CMD uvicorn ocr-app:app --host=0.0.0.0 --port=5000 --reload