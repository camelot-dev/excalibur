.PHONY: docs

install:
	$(INSTALL)
	pip install --upgrade pip
	pip install ".[dev]"

test:
	pytest --verbose --cov-config .coveragerc --cov-report term --cov-report xml --cov=camelot tests

docs:
	cd docs && make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"

publish:
	pip install twine
	python setup.py sdist
	twine upload dist/*
	rm -fr build dist .egg camelot_py.egg-info
