.PHONY: all clean build test-upload upload

clean:
	rm -rf dist

build: clean
	python setup.py sdist

test-upload:
	twine upload --repository testpypi dist/*

upload:
	twine upload --repository pypi dist/*
