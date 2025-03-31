VENV=../.venv
PYTHON=${VENV}/bin/python3.12
PIP=${VENV}/bin/pip

$(VENV)/bin/activate:
	@echo "Creating virtual environment..."
	python -m venv $(VENV)
	$(PIP) install --upgrade pip

install: $(VENV)/bin/activate
	@echo "Installing dependencies..."
	$(PIP) install -r requirements.txt

test:
	$(PYTHON) -m pytest tests/
lint:
	$(PYTHON) -m flake8 src/
format:
	$(PYTHON) -m black src/
build: install lint test

