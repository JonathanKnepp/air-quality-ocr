FROM python:3.10.12 AS air-quality-ocr

# Build environment variables
ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=DontWarn

# Initial setup for container (apt packages, etc.)
COPY ./docker/build/initial.sh ./docker/build/initial.sh
RUN bash ./docker/build/initial.sh

WORKDIR /opt/app

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . .

CMD ["/bin/bash", "scripts/docker/build/entrypoint.sh"]
