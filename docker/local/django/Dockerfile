FROM python:3.13-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements/ requirements/

RUN pip install --no-cache-dir -r requirements/local.txt

COPY . .

COPY ./docker/local/django/entrypoint.sh /entrypoint.sh
COPY ./docker/local/django/start.sh /start.sh


RUN chmod +x /entrypoint.sh /start.sh

ENTRYPOINT [ "/entrypoint.sh" ]