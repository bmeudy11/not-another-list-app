FROM python:3.9

LABEL maintainer="newtonmccollum@gmail.com"

WORKDIR /src

# Install system dependencies needed to build Python packages with C extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libyaml-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, and wheel BEFORE installing requirements
RUN pip install --upgrade pip setuptools wheel

COPY ./src/requirements.txt /src
# Install requirements with --no-cache-dir to reduce layer size and avoid cache issues
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/ /src

CMD ["python", "./main.py"]