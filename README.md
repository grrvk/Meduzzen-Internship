## Meduzzen Internship

### SERVER
to start server:\
uvicorn app.main:app --reload

to run tests:\
python -m pytest

### DOCKER:
to launch with Docker:\
docker-compose build\
docker-compose up

to run tests:\
docker build -f Dockerfile.tests -t app_tests . \
docker run app_tests

### ALEMBIC:
to generate version:\
alembic revision --autogenerate -m "_version name_" \
to run migration:\
alembic upgrade _revision_