FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

ENV PYTHONPATH "${PYTHONPATH}:/"

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --upgrade -r /app/requirements.txt

COPY . .

CMD ["gunicorn", "--workers=3", "-b 0.0.0.0:2000", "-k uvicorn.workers.UvicornWorker", "main:app"]