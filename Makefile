migrate:
	docker compose -f docker-compose.prod.yml run --rm backend python3 manage.py migrate

makemigrations:
	docker compose -f docker-compose.prod.yml exec -T backend python3 manage.py makemigrations
	sudo chown -R $USER:$(id -gn $USER) backend/src/app/migrations/

createsuperuser:
	docker compose -f docker-compose.prod.yml exec -T backend python3 manage.py createsuperuser

collectstatic:
	docker compose -f docker-compose.prod.yml exec -T backend python3 manage.py collectstatic --no-input

dev:
	docker compose -f docker-compose.prod.yml exec -T backend python3 manage.py runserver 0.0.0.0:8000

piplock:
	pipenv install
	sudo chown -R $USER:$(id -gn $USER) backend/Pipfile.lock

up:
	docker compose -f docker-compose.prod.yml up -d

down:
	docker compose -f docker-compose.prod.yml down

restart:
	docker compose -f docker-compose.prod.yml restart backend-app
