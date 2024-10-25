
# Pull official base Python Docker image
FROM python:3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install system dependencies including netcat
RUN apt-get update && \
    apt-get install -y netcat-traditional && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Instala uWSGI
RUN pip install uwsgi

# Copy the Django project
COPY . /code

# Create static and media directories and set permissions
RUN mkdir -p /code/aquinus/staticfiles /code/aquinus/media && \
    chmod -R 755 /code/aquinus/staticfiles /code/aquinus/media

# Set permissions for the entire code directory
RUN chmod -R 755 .