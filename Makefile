install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	pytest -vv --cov=main --cov=utils --cov=scripts tests/test_*.py

format:
	black . *.py

lint:
	pylint --disable=R,C,W1401 *.py utils/*.py tests/*.py scripts/*.py

#container-lint:
#	docker run -rm -i hadolint/hadolint < Dockerfile

refactor:
	format lint

deploy:
	echo "deploy not implemented"

all: install lint test format 
