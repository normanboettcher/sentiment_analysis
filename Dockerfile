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

COPY pip.conf /etc/
RUN pip install  --upgrade pip setuptools

COPY common-requirements.txt /apps
COPY sentiment-model/requirements.txt /apps/sentiment-model/
COPY rest-api/requirements.txt /apps/rest-api/
#install required dependencies first
RUN pip install -r common-requirements.txt \
    -r sentiment-model/requirements.txt \
    -r rest-api/requirements.txt

#copy rest of code
COPY sentiment-model ./sentiment-model/
COPY rest-api ./rest-api/
#install sentiment-model
WORKDIR /apps/sentiment-model
RUN pip install ./
#install rest-api
WORKDIR /apps/rest-api
RUN pip install ./

# ---- Runtime image ----
FROM python:3.12-slim AS runtime

ENV M7_MODEL_PATH=/app/resources/Sentiment-M7.keras
ENV LOOKUP_TABLE_PATH=/app/resources/lookup_table.json
ENV MODEL_NUM_OOV_BUCKETS=1000
ENV MODEL_VOCAB_SIZE=10000

WORKDIR /app
RUN mkdir /resources

COPY sentiment-model/models/Sentiment-M7.keras sentiment-model/lookup_table.json ./resources/

COPY --from=build /apps/rest-api/src ./rest-api/src
COPY --from=build /apps/rest-api/requirements.txt ./rest-api/
COPY --from=build /apps/rest-api/pyproject.toml ./rest-api/
COPY --from=build /apps/sentiment-model/src ./sentiment-model/src
COPY --from=build /apps/sentiment-model/requirements.txt ./sentiment-model/
COPY --from=build /apps/sentiment-model/pyproject.toml ./sentiment-model/

COPY ./common-requirements.txt .

RUN pip install  --upgrade pip && \
    pip install  -r common-requirements.txt

WORKDIR /app/rest-api

RUN pip install  -r requirements.txt && \
    pip install  ../sentiment-model && \
    pip install  .

RUN rm -rf build

#sentiment-model is redundant now
RUN rm -rf ../sentiment-model && \
    rm pyproject.toml requirements.txt && \
    rm ../common-requirements.txt
#workdir with source files
WORKDIR /app/rest-api/src/model_api
#expose port
EXPOSE 5000

ENTRYPOINT ["python", "main.py", "Production"]