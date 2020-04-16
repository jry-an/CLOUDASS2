.PHONY: e2e

VERSION=e2e-test

.PHONY: all
all: deploy

.PHONY: deploy
deploy:
	appcfg.py update . -A $(GAE_PROJECT) --version=$(VERSION)

.PHONY: e2e_test
e2e_test: export GUESTBOOK_URL = http://$(VERSION)-dot-$(GAE_PROJECT).appspot.com
e2e_test: deploy
	pip install -r e2e/requirements-dev.txt
	python e2e/test_e2e.py