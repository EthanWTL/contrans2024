# syntax=docker/dockerfile:1

# Use python bookworm as the base image
FROM python:3.12.5-bookworm

# Set the working directory to /app
WORKDIR /contrans2024

# Copy the requirements.txt file into the container
COPY requirements.txt requirements.txt

# Install Python 3.12.5
RUN pip install --upgrade pip && pip3 install -r requirements.txt

# Expose the port for Jupyter Lab
EXPOSE 8888

# Run Jupyter Lab when the container starts
CMD ["jupyter", "lab", "--allow-root", "--ip=0.0.0.0", "--port=8888"]