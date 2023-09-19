FROM python:3.11-slim-buster


RUN mkdir /internship_fastapi_app


WORKDIR /internship_fastapi_app

COPY requirements.txt .
COPY requirements_dev.txt .


RUN pip install --no-cache-dir --upgrade -r requirements_dev.txt


COPY . .

CMD ["python", "app/main.py"]