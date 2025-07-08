.PHONY: model-api sentiment-model build

sentiment-model:
	@echo "Building sentiment model..."
	@cd sentiment-model && python -m tox --workdir ./sentiment-model --recreate --parallel --skip-missing-interpreters
	@echo "Sentiment model build complete."

model-api:
	@echo "Building model API..."
	@cd rest-api && python -m tox --workdir ./rest-api --recreate --parallel --skip-missing-interpreters
	@echo "Model API build complete."

build: sentiment-model model-api
	@echo "Build process completed for both model API and sentiment model."