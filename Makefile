DOCKER_COMPOSE_FILE=../docker-compose.yaml

lint:
	ruff check app/
	isort --check-only app/ tests/
	black --check app/ tests/

lint-fix:
	ruff check --fix app/
	isort app/ tests/
	black app/ tests/

pre-commit:
	pre-commit autoupdate
	pre-commit run --all-files

create-migrations:
	@PYTHONPATH=$PYTHONPATH:$(pwd) alembic revision --autogenerate -m $(msg)

run-migrations:
	@PYTHONPATH=$PYTHONPATH:$(pwd) alembic upgrade head

rollback-migrations:
	@PYTHONPATH=$PYTHONPATH:$(pwd) alembic downgrade $(id)

start:
	@docker compose -f $(DOCKER_COMPOSE_FILE) up --build -d

stop:
	@docker compose -f $(DOCKER_COMPOSE_FILE) down

tests:
	@docker exec -it api pytest -p no:warnings /api/app/tests


kabum:
	@docker system prune -a --force
	@docker volume prune -a --force
	@if [ -n "$$(docker ps -aq)" ]; then docker stop $$(docker ps -aq); fi
	@if [ -n "$$(docker ps -aq)" ]; then docker rm $$(docker ps -aq); fi
	@if [ -n "$$(docker images -q)" ]; then docker rmi $$(docker images -q); fi
	@if [ -n "$$(docker volume ls -q)" ]; then docker volume rm $$(docker volume ls -q); fi
