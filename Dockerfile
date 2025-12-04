# Build docker container with yafowil.demo
# Run:
#     make install
#     docker compose build

FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN rm -rf /app/venv
RUN python -m venv /app/venv
RUN /app/venv/bin/pip install -r /app/requirements-mxdev.txt

EXPOSE 8080

CMD ["/app/venv/bin/gunicorn", "yafowil.demo:app", "-t", "3600", "-b", "0.0.0.0:8080"]
