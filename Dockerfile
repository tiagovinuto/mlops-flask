# Use a lightweight Alpine Linux image with Python 3.11
FROM python:3.11-alpine

# Install build dependencies and update package repository
RUN apk add --no-cache build-base && apk update

# Install Python packages using pip
RUN pip install --upgrade pip \
    numpy pandas scikit-learn matplotlib seaborn plotly

# Setup a base final image from miniconda
FROM continuumio/miniconda3 as prefect-conda

# Expose Jupyter Notebook port
EXPOSE 8888

VOLUME /DS_PROJECTS
# Copy requirements.txt (if any) and install project dependencies
COPY requirements.txt /DS_PROJECTS/requirements.txt
