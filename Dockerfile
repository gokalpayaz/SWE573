FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN apt-get update && apt-get install -y binutils libproj-dev gdal-bin
RUN pip install -r requirements.txt
COPY . /app