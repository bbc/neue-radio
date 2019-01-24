.PHONY: all source release local run-local deploy

COMPONENT="tne-prototype"

all: local

ext: ../server/requirements.txt
	# Download any PyPI packages listed in requirements.txt to the
	# ext folder.  The extra shell commands catch any errors and ensure
	# the ext folder is not left in a partially complete state.
	( mkdir -p $@ && pip install --download $@ --requirement $< ) || ( rm -rf $@; exit 1 )

source:
	# Bundle up all the source code into a single .tar.gz file, used in
	# combination with the .spec file to create the RPM(s)
	mkdir -p SOURCES
	tar --exclude ".gitignore" --exclude "*.py[co]" --exclude "node_modules" -czf SOURCES/src.tar.gz infrastructure bake-scripts systemd

release: source
	# Clean out any old RPMs from previous builds
	rm -rf SRPMS RPMS
	# Build the package in an fresh CentOS 7 build environment, containing
	# just the RPMs listed as build dependencies in the .spec file.  See
	# https://github.com/bbc/bbc-mock-tools for more information.  Also
	# adds an extra part to the version string containing an
	# auto-incrementing build number.
	$(eval RELEASE_NUM := $(shell cosmos-release generate-version $(COMPONENT)))
	mock-build --os 7 --define "buildnum $(RELEASE_NUM)"
	# Send the RPM and other release metadata to Cosmos.  See
	# https://github.com/bbc/cosmos-release/ for more information
	cosmos-release service $(COMPONENT) RPMS/*.rpm

local: source
	# Build the RPMs locally, without any interaction with the Cosmos component
	rm -rf SRPMS RPMS
	mock-build --os 7

venv: ../server/requirements.txt
	type virtualenv >/dev/null
	(virtualenv $@ && $@/bin/pip install -r $<) || rm -rf $@

run-local: venv
	PYTHONPATH=. venv/bin/python -m helloworld.server

# test: venv/test
#	venv/test/bin/nosetests -v test/

deploy_int:
	cosmos deploy $(COMPONENT) int -f
	cosmos deploy-progress $(COMPONENT) int

deploy_test:
	cosmos deploy $(COMPONENT) test -f
	cosmos deploy-progress $(COMPONENT) test

deploy_live:
	cosmos deploy $(COMPONENT) live -f
	cosmos deploy-progress $(COMPONENT) live
