# Creating image based on the official Python 3 image
FROM python:3.12.4

# Fix Python printing
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /usr/src/app

# Installing all python dependencies
ADD requirements/ requirements/
RUN pip install --no-cache-dir -r requirements/local.txt

# Get the django project into the docker container
ADD ../../ .

# Run Django's server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]