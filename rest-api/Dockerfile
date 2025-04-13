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
COPY . /apps/
#run build for necessary sentiment-model package

RUN tox

# ---- Runtime image ----
FROM python:3.12-slim AS runtime
WORKDIR /app
COPY --from=build /apps/rest-api rest-api
COPY --from=build /apps/sentiment-model sentiment-model

#install only runtime deps
RUN pip install --no-cache-dir --upgrade pip
WORKDIR /app/rest-api
RUN pip install -r requirements.txt
RUN pip install ../sentiment-model
RUN pip install .

RUN rm -rf ../sentiment-model

WORKDIR /app/rest-api/src/model_api
#expose port
EXPOSE 5000
ENTRYPOINT ["python", "main.py"]
CMD ["Production"]


