# Pull base image
FROM duffn/python-poetry:3.10.2-slim-1.2.1-2022-09-19

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV STAGE development

# Copy only requirements to cache them in docker layer
WORKDIR /code

COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$STAGE" == development && echo "--with dev") --no-interaction --no-ansi

# Copy project
COPY . .

# Give execution rights to start script
RUN chmod +x /code/run_server.sh
