.PHONY: docs

install:
	pip install --upgrade pip
	pip install ".[dev]"

test:
	pytest --verbose --cov-config .coveragerc --cov-report term --cov-report xml --cov=excalibur tests

docs:
	cd docs && make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"

publish:
	pip install twine
	python setup.py sdist bdist_wheel --universal
	twine upload dist/*
	rm -rf build dist .egg excalibur_py.egg-info

build-executable:
	pip install pyinstaller
	# https://pythonhosted.org/PyInstaller/when-things-go-wrong.html#helping-pyinstaller-find-modules
	# pyi-makespec --paths=excalibur/executors/celery_executor.py arthur.py
	# replace : with ; for Windows
	pyinstaller --hidden-import="pkg_resources.py2_warn" --add-data "excalibur/www/templates:excalibur/www/templates" --add-data "excalibur/www/static:excalibur/www/static" --add-data "excalibur/config_templates:excalibur/config_templates" arthur.py
