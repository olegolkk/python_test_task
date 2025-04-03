FROM python:3.13

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client
RUN pip install poetry

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi

COPY . .

RUN chmod +x docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]

CMD ["sh", "-c", "until pg_isready -h db; do sleep 2; done && \
     python main.py"]