NAME:="tr-05-docker-relay"
PORT:="9090"

all: test build

run: # app locally
	cd src; python -m main; cd -

black:
	black src/ -l 90 -t py311 --skip-magic-trailing-comma --exclude=payloads_for_tests.py
lint:
	pre-commit run --all-files
lint_config:
	HOMEBREW_NO_AUTO_UPDATE=1; brew install pre-commit && pre-commit install
test: lint
	cd src; coverage run --source api/ -m pytest --verbose ../unittests/ && coverage report --fail-under=80; cd -
test_lf:
	cd src; coverage run --source api/ -m pytest --verbose -vv --lf ../unittests/ && coverage report --fail-under=80; cd -

build: stop
	docker build -q -t $(NAME) .;
	docker run -dp $(PORT):$(PORT) --name $(NAME) $(NAME)
scout:
	docker scout cves $(NAME)
stop:
	docker stop $(NAME); docker rm $(NAME); true

# --------------------------------------------------------------------- #
# If ngrok can be used by you then you can run below make commands
# --------------------------------------------------------------------- #
up: down build expose
down: unexpose stop

expose:
	ngrok http $(PORT) > /dev/null &
echo_ngrok:
	curl -s localhost:4040/api/tunnels | jq -r ".tunnels[0].public_url"
unexpose:
	pkill ngrok; true
