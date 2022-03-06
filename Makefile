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
	@echo "\n${BLUE}Running Bandit against source files...${NC}\n"
	@bandit -r --ini setup.cfg

clean:
	rm -rf .pytest_cache .coverage .pytest_cache coverage.xml reports

veryclean: clean
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf

.PHONY: clean test lint
