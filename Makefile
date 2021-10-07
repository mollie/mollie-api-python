# use virtualenv or virtualenv-wrapper location based on availability
ifdef TRAVIS
	VIRTUALENV := $(VIRTUAL_ENV)
endif
ifdef WORKON_HOME
	VIRTUALENV = $(WORKON_HOME)/mollie-api-python
endif
ifndef VIRTUALENV
	VIRTUALENV = $(PWD)/env
endif

PYTHON_VERSION = 3.9
PYTHON = $(VIRTUALENV)/bin/python


.PHONY: virtualenv
virtualenv: $(VIRTUALENV)  # alias
$(VIRTUALENV):
	$(shell which python$(PYTHON_VERSION)) -m venv $(VIRTUALENV)
	$(PYTHON) -m pip install --upgrade pip setuptools wheel


.PHONY: develop
develop: virtualenv
	$(PYTHON) -m pip install .


.PHONY: test
test: develop
	$(PYTHON) -m pip uninstall --yes pipenv numpy  # travis has some packages preinstalled that are marked vulnerable by safety, and we don't use them
	$(PYTHON) -m pip install -r test_requirements.txt
	$(PYTHON) -m pytest --black --mypy
	$(PYTHON) -m safety check


.PHONY: clean
clean:
	rm -f -r $(VIRTUALENV)
	rm -f -r build/ dist/ .eggs/ mollie_api_python.egg-info .pytest_cache
