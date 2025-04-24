# ---- Base image for build and test ----
FROM python:3.12-slim AS builder

#set environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /apps

COPY common-requirements.txt /apps
COPY sentiment-model/requirements.txt /apps/sentiment-model/
COPY rest-api/requirements.txt /apps/rest-api/
COPY pip.conf /etc/

RUN python -m venv /opt/venv
#activate venv
ENV PATH="/opt/venv/bin:$PATH"
#install dependencies
RUN pip install  --upgrade pip setuptools

#install required dependencies first
RUN pip install -r common-requirements.txt \
    -r sentiment-model/requirements.txt \
    -r rest-api/requirements.txt

#copy rest of code
COPY sentiment-model ./sentiment-model/
#install sentiment-model
WORKDIR /apps/sentiment-model
RUN pip install .

COPY rest-api ./rest-api/
#install rest-api
WORKDIR /apps/rest-api
RUN pip install .

# ---- Runtime image ----
FROM python:3.12-slim AS runtime

ENV M7_MODEL_PATH=/app/resources/Sentiment-M7.keras
ENV LOOKUP_TABLE_PATH=/app/resources/lookup_table.json
ENV MODEL_NUM_OOV_BUCKETS=1000
ENV MODEL_VOCAB_SIZE=10000

WORKDIR /app
RUN mkdir /resources

COPY sentiment-model/models/Sentiment-M7.keras sentiment-model/lookup_table.json ./resources/

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

#expose port
EXPOSE 5000

ENTRYPOINT ["python", "-m", "model_api.main", "Production"]