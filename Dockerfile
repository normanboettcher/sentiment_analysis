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

RUN pip install  --upgrade pip setuptools pytest pytest-cov flake8 black

COPY common-requirements.txt /apps
COPY sentiment-model/requirements.txt /apps/sentiment-model/
COPY rest-api/requirements.txt /apps/rest-api/
#install required dependencies first
RUN pip install  -r common-requirements.txt && \
    pip install  -r sentiment-model/requirements.txt && \
    pip install  -r rest-api/requirements.txt

#copy rest of code
COPY . /apps
#build and install sentiment-model
WORKDIR /apps/sentiment-model
RUN pip install --no-cache-dir .
RUN pytest --cov=sentiment_model --cov-report=term-missing tests/
RUN flake8 src/
RUN black src/

#build and install rest-api
WORKDIR /apps/rest-api

RUN pip install  .
RUN pytest --cov=model_api --cov-report=term-missing tests/
RUN flake8 src/
RUN black src/

# ---- Runtime image ----
FROM python:3.12-slim AS runtime
WORKDIR /app
COPY --from=build /apps/rest-api/src rest-api/src
COPY --from=build /apps/rest-api/requirements.txt rest-api/
COPY --from=build /apps/rest-api/pyproject.toml rest-api/
COPY --from=build /apps/sentiment-model sentiment-model
COPY ./common-requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r common-requirements.txt

WORKDIR /app/rest-api

RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir ../sentiment-model && \
    pip install --no-cache-dir .

RUN rm -rf build

#sentiment-model is redundant now
RUN rm -rf ../sentiment-model
RUN rm pyproject.toml requirements.txt

#workdir with source files
WORKDIR /app/rest-api/src/model_api
#expose port
EXPOSE 5000

ENTRYPOINT ["python", "main.py"]
CMD ["Production"]