.PHONY: install run debug clean lint lint-strict

CONFIG = config.json

install:
	pip install -r requirements.txt

run:
	python3 pac-man.py $(CONFIG)

debug:
	python3 -m pdb pac-man.py $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict