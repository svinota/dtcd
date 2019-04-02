##
#
#

##
# Project version and release
#
version ?= 0.1
release := $(shell git describe | sed 's/-[^-]*$$//;s/-/.post/')
##
# Python-related configuration
#
python ?= python
flake8 ?= flake8
setuplib ?= distutils.core
##
# Python -W flags:
#
#  ignore  -- completely ignore
#  default -- default action
#  all     -- print all warnings
#  module  -- print the first warning occurence for a module
#  once    -- print each warning only once
#  error   -- fail on any warning
#
#  Would you like to know more? See man 1 python
#
wlevel ?= once

##
# Other options
#
# root      -- install root (default: platform default)
# lib       -- lib installation target (default: platform default)
# coverage  -- whether to produce html coverage (default: false)
# pdb       -- whether to run pdb on errors (default: false)
# module    -- run only the specified test module (default: run all)
#
ifdef root
	override root := "--root=${root}"
endif

ifdef lib
	override lib := "--install-lib=${lib}"
endif

all:
	@echo targets:
	@echo
	@echo \* clean -- clean all generated files
	@echo \* install -- install lib into the system
	@echo \* develop -- run \"setup.py develop\" \(requires setuptools\)
	@echo

clean: clean-version
	@rm -rf dist build MANIFEST
	@rm -rf dtcd.egg-info
	@find dtcd -name "*pyc" -exec rm -f "{}" \;
	@find dtcd -name "*pyo" -exec rm -f "{}" \;

setup.ini:
	@awk 'BEGIN {print "[setup]\nversion=${version}\nrelease=${release}\nsetuplib=${setuplib}"}' >setup.ini

clean-version:
	@rm -f setup.ini

force-version: clean-version update-version

update-version: setup.ini

upload: clean force-version
	${python} setup.py sdist
	${python} -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

dist: clean force-version
	@${python} setup.py sdist >/dev/null 2>&1

install: clean force-version
	${python} setup.py install ${root} ${lib}

# in order to get it working, one should install the project
# with setuplib=setuptools, otherwise the project files
# will be silently left not uninstalled
uninstall: clean
	${python} -m pip uninstall dtcd

develop: setuplib = "setuptools"
develop: clean force-version
	${python} setup.py develop
