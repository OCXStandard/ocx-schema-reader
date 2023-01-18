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

#BUILD_DATE = `date +%D.%T`
## Determine which VENV to use
#ifeq ($(OS),Windows_NT)
#	VENV = ${WIN_ENV}
#else
#    VENV = ${MACOS_ENV}
#endif

# CONDA TASKS ##################################################################
# PROJECT setup using conda and powershell
.PHONY: conda-dev
conda-dev:  ## Create a conda development environment from environment.yaml and install all packages
	@conda env create -f environment.yaml
	# ~/.conda.bash_env is a one-liner: eval "$(/path/to/bin/conda shell.bash hook)"
	#export BASH_ENV=${HOME}\.conda.bash_env
cd: conda-dev
.PHONY: cd
conda-upd:  environment.yaml ## Update the conda development environment when environment.yaml has changed
	@conda env update -f environment.yaml
cu: conda-upd
.PHONY:cu

conda-lock:  environment.yaml ## Update the conda development environment when environment.yaml has changed
	@conda env export > environment.lock.yaml

cl: conda-lock
.PHONY: cl

conda-activate: ## Activate the conda environment for the project
	@conda activate ocx
ca: conda-activate
.PHONY: ca

# PROJECT DEPENDENCIES ########################################################

# VIRTUAL_ENV ?= ${VENV}
# DEPENDENCIES := $(VIRTUAL_ENV)/$(shell cksum pyproject.toml)


# Color output
BLUE='\033[0;34m'
NC='\033[0m' # No Color


var:
	@printf "${BLUE}${SPHINXBUILD}"
	@printf "${BLUE}${BUILDDIR}"
	@printf "${BLUE}${SOURCEDIR}"
	@printf "${BLUE}${SPHINXOPTS}"
	@printf "${BLUE}${UMNAME}"

.PHONY: var


# RUN ##################################################################

PHONY: run
run: ## Start ocx-tools CLI
	python main.py

# TESTS #######################################################################

FAILURES := .pytest_cache/pytest/v/cache/lastfailed

test:  ## Run unit and integration tests
	@pytest --durations=5  --cov-report html --cov ocx_tools .

test-upd:  ## Update the regression tests baseline
	@pytest --force-regen

tu: test-upd
PHONY: tu

test-cov:  ## Show the test coverage report
	cmd /c start $(CURDIR)/$(COVDIR)/index.html

tc: test-cov
.PHONY: tc

PHONY: test-upd, test-cov
# CHECKS ######################################################################
check-lint:	## Run formatters, linters, and static code security scanners bandit and jake
	@printf "\n${BLUE}Running black against source and test files...${NC}\n"
	@black . -v
	@printf "${BLUE}\nRunning Flake8 against source and test files...${NC}\n"
	@flake8 -v
	@printf "${BLUE}\nRunning Bandit against source files...${NC}\n"
	bandit -r -v -c pyproject.toml ocx_schema_reader
	@printf "${BLUE}\nRunning Jake against installed dependencies...${NC}\n"
	conda list | jake ddt | grep VULNERABLE

cl: check-lint
.PHONY: cl

check-jake:   ## Detailed report from jake security scanner on all modules installed in the conda environment
	@printf "${BLUE}\nRunning Jake against installed dependencies...${NC}\n"
	conda list | jake ddt

cj: check-jake
.PHONY: cj

# DOCUMENTATION ##############################################################
SPHINXBUILD = python -m sphinx
SPHINXOPTS = "html"
SOURCEDIR = "$(CURDIR)/docs/source"
BUILDDIR =  "$(CURDIR)/docs/build/"
COVDIR = "htmlcov"

doc-serve: ## Open the the html docs built by Sphinx
	@cmd /c start "$(BUILDDIR)$(SPHINXOPTS)/index.html"

ds: doc-serve
.PHINY: ds

doc-help:  ## Sphinx options when running make from the docs folder
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

doc: ## Build the html docs using Sphinx. For other Sphinx options, run make in the docs folder
	@$(SPHINXBUILD)  -M clean "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@$(SPHINXBUILD)  "$(SOURCEDIR)" "$(BUILDDIR)/$(SPHINXOPTS)" -b "$(SPHINXOPTS)"


# BUILD #######################################################################

DIST_FILES := dist/*.tar.gz dist/*.whl
EXE_FILES := dist/$(PACKAGE).*

build-exe:   ## Build a bundled package (on windows: an exe file) executable using pyinstaller
	pyinstaller main.spec


bump-dev:  ## Bump the version the next version. All version strings will be updated
	@bump2version --config-file .bumpversion.cfg -n  part dev --new-version  $($1)



# HELP ########################################################################


.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

#-----------------------------------------------------------------------------------------------



