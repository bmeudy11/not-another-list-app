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

# Install test requirements with pip cache disabled and prefer binary wheels
RUN pip install --no-cache-dir --prefer-binary --disable-pip-version-check -U requests pytest

COPY wait-for-it.sh /
RUN chmod +x /wait-for-it.sh

COPY ./src/ /src

# TODO: Update API Path to be an ENV/ARG in the Dockerfile
CMD ["/wait-for-it.sh" , "natl_backend_api:8081" , "--strict" , "--timeout=300" , "--" ,"pytest", "/src/"]
