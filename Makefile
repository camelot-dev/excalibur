.PHONY: install test lint docs build-executable

install:
	uv sync --extra dev

test:
	uv run pytest

lint:
	uvx pre-commit run --all-files

docs:
	cd docs && make html

build-executable:
	pip install pyinstaller
	# https://pythonhosted.org/PyInstaller/when-things-go-wrong.html#helping-pyinstaller-find-modules
	# pyi-makespec --paths=excalibur/executors/celery_executor.py arthur.py
	# replace : with ; for Windows
	pyinstaller --hidden-import="pkg_resources.py2_warn" --add-data "excalibur/www/templates:excalibur/www/templates" --add-data "excalibur/www/static:excalibur/www/static" --add-data "excalibur/config_templates:excalibur/config_templates" arthur.py
