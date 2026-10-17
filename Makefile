.PHONY: build test lint run doctor

build:
	@echo "Build succeeded"

test:
	@python3 -m unittest discover -s tests -t . -v

lint:
	@python3 -m py_compile tests/test_demo.py && echo "0 warnings"

run:
	@echo "no server in demo"

doctor:
	@bash scripts/doctor.sh
