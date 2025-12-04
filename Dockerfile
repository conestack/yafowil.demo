FROM python:3.13-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

COPY . /app

# Install gunicorn
RUN pip install --no-cache-dir gunicorn

RUN pip install ./sources/odict
RUN pip install ./sources/plumber
RUN pip install ./sources/node
RUN pip install ./sources/webresource
RUN pip install ./sources/treibstoff
RUN pip install ./sources/yafowil
RUN pip install ./sources/yafowil.bootstrap
RUN pip install ./sources/yafowil.lingua
RUN pip install ./sources/yafowil.webob
RUN pip install ./sources/yafowil.widget.ace
RUN pip install ./sources/yafowil.widget.array
RUN pip install ./sources/yafowil.widget.autocomplete
RUN pip install ./sources/yafowil.widget.color
RUN pip install ./sources/yafowil.widget.cron
RUN pip install ./sources/yafowil.widget.datetime
RUN pip install ./sources/yafowil.widget.dict
RUN pip install ./sources/yafowil.widget.image
RUN pip install ./sources/yafowil.widget.location
RUN pip install ./sources/yafowil.widget.select2
RUN pip install ./sources/yafowil.widget.slider
RUN pip install ./sources/yafowil.widget.tiptap
RUN pip install ./sources/yafowil.yaml
RUN pip install .

EXPOSE 8080

CMD ["gunicorn", "yafowil.demo:app", "-t", "3600", "-b", "0.0.0.0:8080"]
