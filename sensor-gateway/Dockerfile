FROM python:3.10.7-slim-buster

WORKDIR /code

COPY ./Pipfile /code/Pipfile
COPY ./Pipfile.lock /code/Pipfile.lock

RUN export PIP_NO_CACHE_DIR=false

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

COPY . /code/

CMD ["uvicorn", "src.app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "9500"] 