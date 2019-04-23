# use virtualenv or virtualenv-wrapper location based on availability
ifdef TRAVIS
	VIRTUALENV := $(VIRTUAL_ENV)
endif
ifdef WORKON_HOME
	VIRTUALENV = $(WORKON_HOME)/mollie-api-python
endif
ifndef VIRTUALENV
	VIRTUALENV = $(PWD)/venv
endif

PYTHON = $(VIRTUALENV)/bin/python


.PHONY: virtualenv
virtualenv: $(VIRTUALENV)  # alias
$(VIRTUALENV):
	virtualenv $(VIRTUALENV)
	$(PYTHON) -m pip install --upgrade pip setuptools


.PHONY: develop
develop: virtualenv
	$(PYTHON) -m pip install .


.PHONY: test
test: develop
	$(PYTHON) -m pip install pytest pytest-cov responses mock pyflakes pycodestyle isort safety
	$(PYTHON) -m pytest
	$(PYTHON) -m pyflakes examples mollie tests
	$(PYTHON) -m pycodestyle examples mollie tests
	$(PYTHON) -m isort --recursive --check-only examples mollie tests
	$(PYTHON) -m safety check --ignore 36810  # travis has vulnerable numpy==1.15.4 pre-installed that we don't use


.PHONY: clean
clean:
	rm -f -r $(VIRTUALENV)
	rm -f -r dist/ .eggs/ mollie_api_python.egg-info .pytest_cache
