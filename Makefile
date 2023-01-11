# A self-documenting Makefile
# You can set these variables from the command line, and also
# from the environment for the first two.
SOURCE = ./ocx_schema_reader/
# PS replacements for sh
RM = 'del -Confirmed False'

#host-type := $(shell arch)
#MACOS_ENV = .macosenv
#WIN_ENV = .win_env
PACKAGE := ocx_schema_reader
MODULES := $(wildcard $(PACKAGE)/*.py)
COMMIT_HASH = `git rev-parse --short HEAD 2>/dev/null`
SPHINXBUILD = python -m sphinx
SPHINXOPTS = "html"
SOURCEDIR = "$(CURDIR)/docs/source"
BUILDDIR =  "$(CURDIR)/docs/build/"
COVDIR = "htmlcov"
#BUILD_DATE = `date +%D.%T`
## Determine which VENV to use
#ifeq ($(OS),Windows_NT)
#	VENV = ${WIN_ENV}
#else
#    VENV = ${MACOS_ENV}
#endif

# PROJECT setup using conda and powershell
.PHONY: conda-dev
conda-dev:  ## Create a conda development environment from environment.yaml and install all packages
	@conda env create -f environment.yaml
	# ~/.conda.bash_env is a one-liner: eval "$(/path/to/bin/conda shell.bash hook)"
	#export BASH_ENV=${HOME}\.conda.bash_env

.PHONY: conda-upd
conda-upd:  environment.yaml ## Update the conda development environment when environment.yaml has changed
	@conda env update -f environment.yaml

conda-lock:  environment.lock.yaml ## Update the conda development environment when environment.yaml has changed
	@conda env export > environment.lock.yaml
	# ~/.conda.bash_env is a one-liner: eval "$(/path/to/bin/conda shell.bash hook)"
	#export BASH_ENV=${HOME}\.conda.bash_env


# PROJECT DEPENDENCIES ########################################################

# VIRTUAL_ENV ?= ${VENV}
# DEPENDENCIES := $(VIRTUAL_ENV)/$(shell cksum pyproject.toml)


# Color output
BLUE='\033[0;34m'
NC='\033[0m' # No Color


var:  ## List Makefile variables
	@printf "${BLUE}${SPHINXBUILD}"
	@printf "${BLUE}${BUILDDIR}"
	@printf "${BLUE}${SOURCEDIR}"
	@printf "${BLUE}${SPHINXOPTS}"
	@printf "${BLUE}${UMNAME}"




# MAIN TASKS ##################################################################

.PHONY: all
all: install


.PHONY: install

PHONY: run
run: ## Start the ocx-schema-reader CLI
	python main.py

# TESTS #######################################################################

FAILURES := .pytest_cache/pytest/v/cache/lastfailed

test:  ## Run unit and integration tests
	@pytest --durations=5 -v --cov-report html --cov ocx_schema_reader .

test-upd:  ## Update the regression tests baseline
	@pytest --force-regen


test-cov:  ## Show the test coverage report
	cmd /c start $(CURDIR)/$(COVDIR)/index.html

PHONY: test-upd, test-cov
# CHECKS ######################################################################
lint:	## Run formatters, linters, and static code security scanners bandit and jake
	@printf "\n${BLUE}Running black against source and test files...${NC}\n"
	@black . -v
	@printf "${BLUE}\nRunning Flake8 against source and test files...${NC}\n"
	@flake8 -v
	@printf "${BLUE}\nRunning Bandit against source files...${NC}\n"
	bandit -r -v -c pyproject.toml ocx_schema_reader
	@printf "${BLUE}\nRunning Jake against installed dependencies...${NC}\n"
	conda list | jake ddt | grep VULNERABLE

PHONY: lint

jake:   ## Detailed report from jake security scanner on all modules installed in the conda environment
	@printf "${BLUE}\nRunning Jake against installed dependencies...${NC}\n"
	conda list | jake ddt
PHONY: jake

# DOCUMENTATION ##############################################################
html-serve: ## Open the the html docs built by Sphinx
	@cmd /c start "$(BUILDDIR)$(SPHINXOPTS)/index.html"

sphinx-help:  ## Sphinx options
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

doc: ## Build the html docs using Sphinx. For other Sphinx options, run make in the docs folder
	@$(SPHINXBUILD) -M clean "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@$(SPHINXBUILD) -a "$(SOURCEDIR)" "$(BUILDDIR)/$(SPHINXOPTS)" -b "$(SPHINXOPTS)"


# BUILD #######################################################################

DIST_FILES := dist/*.tar.gz dist/*.whl
EXE_FILES := dist/$(PACKAGE).*

build: dist/main.exe
	pyinstaller


bump-dev:  ## Bump the version the next version. All version strings will be updated
	@bump2version --config-file .bumpversion.cfg -n  part dev --new-version  $($1)


# RELEASE #####################################################################

.PHONY: upload
upload: dist ## Upload the current version to PyPI
	git diff --name-only --exit-code
	poetry publish
	bin/open https://pypi.org/project/$(PACKAGE)

# CLEANUP #####################################################################

.PHONY: clean
clean:  .clean-test  ## Delete all generated and temporary files

.PHONY: clean-all
clean-all: clean
	#rm -rf $(VIRTUAL_ENV)

.PHONY: .clean-install
.clean-install:
	find $(PACKAGE) tests -name '*.pyc' -print
	rm -rf *.egg-info

.PHONY: .clean-test
.clean-test:
	@$(RM) .\.pytest_cache\

.PHONY: .clean-docs
.clean-docs:
	rm -rf docs/*.png site

.PHONY: .clean-build
.clean-build:
	rm -rf *.spec dist build

.PHONY: .clean-log
.clean-log:
	rm -rf log/*.log

# HELP ########################################################################


.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

#-----------------------------------------------------------------------------------------------



