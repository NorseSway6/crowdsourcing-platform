FROM python:3.10-slim-buster

WORKDIR /app

RUN pip install pipenv --no-cache-dir
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy && pip cache purge

COPY . .

WORKDIR /app/src
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
