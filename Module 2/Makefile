.PHONY: help build up down logs clean restart shell-backend shell-frontend migrate seed ps

help:
	@echo "Available commands:"
	@echo "  make build          - Build all containers"
	@echo "  make up             - Start all services"
	@echo "  make down           - Stop all services"
	@echo "  make logs           - View logs"
	@echo "  make ps             - List running containers"
	@echo "  make restart        - Restart all services"
	@echo "  make clean          - Remove containers and volumes"
	@echo "  make shell-backend  - Access backend container shell"
	@echo "  make shell-frontend - Access frontend container shell"
	@echo "  make migrate        - Run database migrations"
	@echo "  make seed           - Seed database with demo data"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

ps:
	docker-compose ps

restart:
	docker-compose restart

clean:
	docker-compose down -v
	docker system prune -f

shell-backend:
	docker-compose exec backend /bin/bash

shell-frontend:
	docker-compose exec frontend /bin/sh

migrate:
	docker-compose exec backend uv run alembic upgrade head

seed:
	docker-compose exec backend uv run python -m scripts.seed_db

