FROM python:3.12-slim

# env variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

# working directory will be app
WORKDIR /app

# copy poetry depedencies file
COPY pyproject.toml poetry.lock ./

# install poetry and the specified dependencies within poetry
RUN pip install poetry
RUN poetry install --no-root

# copy application
COPY app app

# copy and run entrypoint script
COPY /scripts/bash/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]