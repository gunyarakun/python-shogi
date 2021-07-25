.PHONY: all clean build test-upload upload

clean:
	rm -rf dist

build: clean
	python setup.py sdist

test-upload: build
	twine upload --repository testpypi dist/*

upload: build
	twine upload --repository pypi dist/*
