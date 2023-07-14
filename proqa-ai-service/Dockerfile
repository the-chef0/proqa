# Dockerfile for proqa-ai-service project
FROM docker.io/python:3.10 as builder

# Add enviroment variables that ensure there is no cache, and the location of the venv
ENV PIP_NO_CACHE_DIR=1
ENV PIPENV_CUSTOM_VENV_NAME=venv
ENV WORKON_HOME=/opt/

# Install pipenv in the builder stage
RUN pip install --user pipenv

WORKDIR /app

# Copy the Pipenv files in
ADD Pipfile.lock Pipfile /app/

# Sync all the dependencies
RUN /root/.local/bin/pipenv sync -d

FROM docker.io/python:3.10-slim as runtime

# Copy the virtualenv from the builder
COPY --from=builder /opt/venv /opt/venv/

ENV PIP_NO_CACHE_DIR=1
ENV PIPENV_CUSTOM_VENV_NAME=venv
ENV WORKON_HOME=/opt/
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV SERVER_PORT=8001
ENV SERVER_HOST=0.0.0.0
EXPOSE 8001

# Set the working directory inside the Docker image
WORKDIR /app

# Copy the contents of the proqa-ai-service project into the container
COPY . .

# Set entrypoint to the start script
ENTRYPOINT ["./docker-entrypoint.sh"]
