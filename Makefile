.PHONY: all clean build test-upload upload test install

clean:
	rm -rf dist

build: clean
	python setup.py sdist

test-upload: build
	twine upload --repository testpypi dist/*

upload: build
	twine upload --repository pypi dist/*

test:
	nosetests

install:
	pip install -r requirements.txt
