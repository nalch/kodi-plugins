VERSION_GREP = | grep \<addon | tr 'A-Z' 'a-z' | sed 's/.*version="\([^"]*\)"*.*/\1/g'
IN_ENV = . .env/bin/activate &&

update-addons: dist
	echo "<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<addons>" > addons.xml && \
	find plugin*/addon.xml -maxdepth 0 -type f -exec sh -c 'cat {} | tail -n +2' >> addons.xml \; && \
	echo "</addons>" >> addons.xml && \
	md5sum addons.xml > addons.xml.md5

dist:
	for PLUGIN_DIR in $$(find plugin* -maxdepth 0 -type d); do \
		VERSION=$$(cat $$PLUGIN_DIR/addon.xml $(VERSION_GREP)); \
		echo "$$PLUGIN_DIR-$$VERSION"; \
		zip -r $$PLUGIN_DIR/$$PLUGIN_DIR-$$VERSION.zip $$PLUGIN_DIR/ -x \*.zip -x \*.git; \
	done

repository:
	set -e ;\
	VERSION=$$(cat repository.nalch/addon.xml $(VERSION_GREP)); \
	zip -r repository.nalch-$$VERSION.zip repository.nalch/ -x \*.zip -x \*.git

env:
	python3 -m venv .env

init: env test_reqs

test_reqs: env
	$(IN_ENV) pip install flake8

test:
	$(IN_ENV) flake8 plugin*/*.py

all: dist update-addons repository
