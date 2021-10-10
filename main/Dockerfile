FROM python:3.9
ENV PYTHONUNBUFFERED=1
RUN apt update && apt install iputils-ping -y
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

