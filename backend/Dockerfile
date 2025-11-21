FROM python:3.9

LABEL maintainer="newtonmccollum@gmail.com"

WORKDIR /src

# Install system dependencies needed to build Python packages with C extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libyaml-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip to latest first, then setuptools and wheel
RUN python -m pip install --no-cache-dir --upgrade 'pip>=24.0' setuptools wheel

COPY ./src/requirements.txt /src

# Install requirements with pip cache disabled and prefer binary wheels  
RUN pip install --no-cache-dir --prefer-binary --disable-pip-version-check -r requirements.txt

COPY ./src/ /src

CMD ["python", "./main.py"]