run:
	docker compose -f local.yml up

runl:
	./manage.py runserver

# Clear all images, container without volumes
clear:
	docker system prune -a

# Clear all data - images, container, volumes
clear-all:
	docker system prune -a && docker volume prune -a

migrate:
	./manage.py migrate

# download fixture data to database
city-load:
	python manage.py loaddata fixtures/cities_fixture.json