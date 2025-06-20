# Execute the "targets" in this file with `make <target>` e.g., `make test`.
#
# You can also run multiple in sequence, e.g. `make clean lint test serve-coverage-report`

install:
	bash run.sh install

generate-project:
	bash run.sh generate-project

lint:
	bash run.sh lint

lint-ci:
	bash run.sh lint:ci

test:
	bash run.sh run-tests

test-wheel-locally:
	bash run.sh test:wheel-locally

clean:
	bash run.sh clean

help:
	bash run.sh help
