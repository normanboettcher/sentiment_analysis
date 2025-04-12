# ---- Base image for build and test ----
FROM python:3.12-slim AS build

#set environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /apps

#install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip setuptools tox
#run build for necessary sentiment-model package
WORKDIR /apps/sentiment-model
COPY ../sentiment-model/pyproject.toml .
COPY ../sentiment-model/setup.cfg .
COPY ../sentiment-model/requirements.txt .
COPY ../sentiment-model/src src/
COPY ../sentiment-model/tests tests/
RUN tox
#run build for rest-api package
WORKDIR /apps/rest-api
COPY pyproject.toml .
COPY setup.cfg .
COPY requirements.txt .
COPY src src/
COPY tests tests/
RUN tox

# ---- Runtime image ----
FROM python:3.12-slim AS runtime
WORKDIR /app
COPY --from=build /apps/rest-api /app

#install only runtime deps
RUN pip install --upgrade pip && \
    pip install .

#expose port
EXPOSE 5000

CMD ["python", "main.py", "Production"]


