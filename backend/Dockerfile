FROM python:3.9

LABEL maintainer="newtonmccollum@gmail.com"

WORKDIR /src

# Install system dependencies needed to build Python packages with C extensions
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libyaml-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY ./src/requirements.txt /src
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

COPY ./src/ /src

CMD ["python", "./main.py"]