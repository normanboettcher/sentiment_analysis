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

RUN python -m venv .venv

RUN . .venv/bin/activate && pip install --upgrade pip setuptools tox

COPY . /apps

#run build for necessary sentiment-model package
RUN . .venv/bin/activate && tox

# ---- Runtime image ----
FROM python:3.12-slim AS runtime
WORKDIR /app
COPY --from=build /apps/rest-api rest-api
COPY --from=build /apps/sentiment-model sentiment-model
COPY ./common-requirements.txt .

RUN rm -rf  /app/rest-api/tests

RUN python -m venv .venv
RUN . .venv/bin/activate && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r common-requirements.txt

WORKDIR /app/rest-api

RUN . ../.venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir ../sentiment-model && \
    pip install --no-cache-dir .

#set path for usage later on
ENV PATH="/app/.venv/bin:$PATH"

#sentiment-model is redundant now
RUN rm -rf ../sentiment-model

WORKDIR /app

#debugging
RUN ls -laR
#workdir with source files
WORKDIR /app/rest-api/src/model_api
#expose port
EXPOSE 5000

ENTRYPOINT ["python", "main.py"]
CMD ["Production"]