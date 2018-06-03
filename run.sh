docker run -d --name ghmonitor_postgres \
           -p 5555:5432 \
           -v $PWD/db.postgres:/var/lib/postgresql/data \
           -e POSTGRES_PASSWORD=ghmonitor \
           -e POSTGRES_USER=ghmonitor \
           postgres

npm run start &

pipenv run python manage.py runserver

docker rm -f ghmonitor_postgres
