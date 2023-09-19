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
if *service "app" is not running*: 
docker-compose up -d --build\
docker-compose exec app pytest .