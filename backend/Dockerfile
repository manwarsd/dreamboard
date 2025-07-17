FROM python:3.12-slim

ENV PYTHONUNBUFFERED True

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY app /code/app

ENV PYTHONPATH "${PYTHONPATH}:/code/app"

# 👇 Fix: main.py is inside app/, so use `app.main:app`
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
