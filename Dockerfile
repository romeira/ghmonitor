FROM python:3.6

COPY Pipfile .
COPY Pipfile.lock .

RUN pip install -U pipenv
RUN pipenv install --dev --system

WORKDIR /app
