FROM python:3.13.0-alpine AS python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=2.1.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


FROM python-base AS builder-base

RUN apk update \
    && apk add --no-cache \
        curl build-base netcat-openbsd

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=${POETRY_VERSION} python3 -
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./
RUN poetry install --only main --no-root
# ??RUN poetry install --without dev,test --no-interaction --no-ansi


FROM python-base AS development
ENV FASTAPI_ENV=development

WORKDIR $PYSETUP_PATH
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

RUN poetry install --no-root
WORKDIR /app
# EXPOSE 8002
ENTRYPOINT ["sh","./entrypoint.sh"]


FROM python-base AS production
ENV FASTAPI_ENV=production
WORKDIR $PYSETUP_PATH
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
# COPY ./$PYSETUP_PATH /$PYSETUP_PATH/
COPY ./app /app/
WORKDIR /app
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app"]
# CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8002", "--workers", "4", "main:app"]
