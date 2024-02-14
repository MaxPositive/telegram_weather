# define an alias for the specific python version used in this file.
FROM python:3.11.7-slim-bullseye as python

# Python build stage
FROM python as python-build-stage

ARG BUILD_ENVIRONMENT=local
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VENV="/opt/poetry-venv"
ENV POETRY_CACHE_DIR="/opt/.cache"

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev \
  # Install poetry
  && python3 -m venv $POETRY_VENV \
  && $POETRY_VENV/bin/pip install -U pip setuptools \
  && $POETRY_VENV/bin/pip install poetry

# Python 'run' stage
FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}
ENV POETRY_VENV="/opt/poetry-venv"

WORKDIR ${APP_HOME}

# Install required system dependencies
RUN apt-get update \
  && apt-get install --no-install-recommends -y \
    libpq-dev \
    gettext \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Copy Poetry to app image
COPY --from=python-build-stage $POETRY_VENV $POETRY_VENV

# Add Poetry to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

COPY ./pyproject.toml ./poetry.lock ${APP_HOME}

RUN poetry check

RUN poetry install --no-interaction --no-cache

COPY ./compose/local/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# copy application code to WORKDIR
COPY . ${APP_HOME}

ENTRYPOINT ["/entrypoint"]

EXPOSE 8000