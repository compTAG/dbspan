MODULE := dbspan
BLUE='\033[0;34m'
NC='\033[0m' # No Color

demo:
	@python -m $(MODULE) dbspan

test:
	@pytest

lint:
	@echo "\n${BLUE}Running Pylint against source and test files...${NC}\n"
	@pylint --rcfile=setup.cfg **/*.py
	@echo "\n${BLUE}Running Flake8 against source and test files...${NC}\n"
	@flake8

.PHONY: clean test lint
