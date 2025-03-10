SHELL := /bin/bash
VERSION := $(shell grep "^version" pyproject.toml | cut -d'=' -f2 | tr -d ' ' | tr -d '"')

test:
	pytest

build:
	python -m build

tag:
	git tag -a v$(VERSION) -m "Release $(VERSION)"

release: test tag
	git push origin v$(VERSION)
