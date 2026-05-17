REGISTRY := ghcr.io
REPO_NAME := $(shell echo $(GITHUB_REPOSITORY) | tr '[:upper:]' '[:lower:]')
SHA := $(shell echo $(GITHUB_SHA) | cut -c1-7)

IMAGE_BACKEND := $(REGISTRY)/$(REPO_NAME)-backend:$(SHA)
IMAGE_FRONTEND := $(REGISTRY)/$(REPO_NAME)-frontend:$(SHA)

migrate:
	docker compose -f docker-compose.prod.yml run --rm backend python3 manage.py migrate

makemigrations:
	docker compose -f docker-compose.prod.yml exec -T backend python3 manage.py makemigrations
	sudo chown -R $USER:$(id -gn $USER) backend/src/app/migrations/

createsuperuser:
	docker compose -f docker-compose.prod.yml exec backend python3 manage.py createsuperuser

collectstatic:
	docker compose -f docker-compose.prod.yml exec -T backend python3 manage.py collectstatic --no-input

dev:
	docker compose -f docker-compose.prod.yml exec -T backend python3 manage.py runserver 0.0.0.0:8000

piplock:
	pipenv install
	sudo chown -R $USER:$(id -gn $USER) backend/Pipfile.lock

lint-backend:
	docker run --rm $(IMAGE_BACKEND) isort .
	docker run --rm $(IMAGE_BACKEND) flake8 --config ../setup.cfg .
	docker run --rm $(IMAGE_BACKEND) black --config ../pyproject.toml .

lint-frontend:
	docker run --rm $(IMAGE_FRONTEND) bun run lint
	docker run --rm $(F_IMAGE) bun x tsc -b
	docker run --rm $(F_IMAGE) bun x prettier --check "src/**/*.{ts,tsx,scss,css}"

build-backend:
	docker image build -t $(IMAGE_BACKEND) ./backend

build-frontend:
	docker image build -t $(IMAGE_FRONTEND) ./frontend

push-backend:
	docker push $(IMAGE_BACKEND)

push-frontend:
	docker push $(IMAGE_FRONTEND)

pull-backend:
	docker pull $(IMAGE_BACKEND)

pull-frontend:
	docker pull $(IMAGE_FRONTEND)

up:
	docker compose -f docker-compose.prod.yml up -d

down:
	docker compose -f docker-compose.prod.yml down

restart:
	docker compose -f docker-compose.prod.yml restart backend-app
