# A self-documenting Makefile
# You can set these variables from the command line, and also
# from the environment for the first two.

SPHINXOPTS    = html
SPHINXBUILD   = sphinx-build
SOURCEDIR     = docs/source
BUILDDIR      = docs/build

MODULE := ocx_schema_reader

COMMIT_HASH = `git rev-parse --short HEAD 2>/dev/null`
BUILD_DATE = `date + %FT%T%Z`


.PHONY: install build export bump sphinx sphinx-help html
.DEFAULT_GOAL := help

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


init: ## Init the project dev set-up. poetry must be installed in the Python environment
	@printf "\033[36m%s\033[0m %s\n, 'Installing flake8 ...'"
	@poetry add flake8
	@printf "\033[36m%s\033[0m %s\n, 'Installing black ...'"
	@poetry add black
	@printf "\033[36m%s\033[0m %s\n, 'Installing isort ...'"
	@poetry add isort
	@printf "\033[36m%s\033[0m %s\n, 'Installing bump2version ...'"
	@poetry self add bump2version


hash:  ## Print the git HASH
	@printf "\033[36m%s\033[0m" $(COMMIT_HASH)

export: requirements_dev.txt ## Export requirements to requirements_dev.txt
	@printf "\033[36m%s\033[0m\n"  'Updating requirements_dev.txt ...'
	@poetry export --without-hashes -o requirements_dev.txt

install: poetry.lock
	@printf "\033[36m%s\033[0m\n"   "Installing dependencies ..."
	@poetry install

build: hash
	@printf "\033[36m%s\033[0m %s\n, 'Building target ...'"
	@poetry build

test-all: ## Run all tests and display the summary
	@pytest --durations=5 -v

lint: ## Run the linters on the source code
	@printf "\033[36m%s\033[0m\n"  "Running black against source and test files..."
	@black . -v
	@printf "\033[36m%s\033[0m\n"  "Running Flake8 against source and test files..."
	@flake8 -v
	@printf "\033[36m%s\033[0m\n"  "\nRunning Isort against source files..."
	@isort .

html: ## Open the the html docs built by Sphinx
	@cmd /c start $(CURDIR)/$(BUILDDIR)/html/$(MODULE).html


# define the name of the virtual environment directory
VENV := venv

# default target, when make executed without arguments
all: install build export

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements.txt

# venv is a shortcut target
venv: $(VENV)/bin/activate

run: venv
	./$(VENV)/bin/python3 app.py

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

bump:  ## Bump the version the next version. All version strings will be updated

sphinx-help:  ## Sphinx options
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

sphinx: ## Build the html docs using Sphinx. For other Sphinx options, run make in the docs folder
	@$(SPHINXBUILD) -M "$(SPHINXOPTS)" "$(SOURCEDIR)" "$(BUILDDIR)"
