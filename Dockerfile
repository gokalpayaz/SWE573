FROM python:3.9
ENV PYTHONUNBUFFERED=1
WORKDIR /django
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y binutils libproj-dev gdal-bin
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 80