# Dockerfile for proqa-back-end project
FROM docker.io/python:3.10.11 as builder

# Add enviroment variables that ensure there is no cache, and the location of the venv
ENV PIP_NO_CACHE_DIR=1
ENV PIPENV_CUSTOM_VENV_NAME=venv
ENV WORKON_HOME=/opt/
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install pipenv in the builder stage
RUN pip install --user pipenv

WORKDIR /app

# Copy the Pipenv files in
ADD Pipfile.lock Pipfile /app/

# Sync all the dependencies
RUN /root/.local/bin/pipenv sync -d

FROM docker.io/python:3.10.11-slim as runtime

# Install the needed packages
RUN apt-get update \ 
    && apt-get install -y libpq5 procps \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Copy the virtualenv from the builder
COPY --from=builder /opt/venv /opt/venv/

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_NO_CACHE_DIR=1
ENV PIPENV_CUSTOM_VENV_NAME=venv
ENV WORKON_HOME=/opt/
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV TIMEOUT=600


# Set the working directory inside the Docker image
WORKDIR /app

# Copy the contents of the proqa-back-end project into the container
COPY . .

# Set the command that is ran when the container is ran
ENTRYPOINT ["./docker-entrypoint.sh"]