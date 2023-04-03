.PHONY: all test-upload upload test install-poetry install format

test-upload:
	poetry publish --build -r testpypi

upload:
	poetry publish --build -r pypi

test:
	poetry run nosetests

install-poetry:
	curl -sSL https://install.python-poetry.org | python -

install: install-poetry
	git config --local core.hooksPath .githooks
	pip install -r requirements.txt

format:
	poetry run isort . && poetry run black . && poetry run pflake8 .
