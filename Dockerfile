FROM python:3-alpine

WORKDIR /usr/src/app

COPY docker-net-graph.py Pipfile Pipfile.lock ./

RUN pip install pipenv
RUN pipenv install --system --deploy

CMD ["python", "docker-net-graph.py"]