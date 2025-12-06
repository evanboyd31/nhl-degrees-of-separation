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
COPY . .

RUN chmod +x /app/scripts/entrypoint.sh
ENTRYPOINT ["/app/scripts/entrypoint.sh"]