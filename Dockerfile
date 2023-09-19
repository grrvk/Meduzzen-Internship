FROM python:3.11


WORKDIR /internship_fastapi_app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["python", "app/main.py"]