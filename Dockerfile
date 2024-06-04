FROM python:3.12-slim-bullseye

RUN apt-get update && \
  apt-get install -y python3-setuptools && \
  apt-get purge python3-pip && \
  rm -rf /var/cache/apt

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]