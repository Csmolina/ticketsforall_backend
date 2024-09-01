FROM python:3.12


COPY pyproject.toml .
COPY poetry.lock .
COPY README.md .

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install

COPY adapters ./adapters
COPY api ./api
COPY core ./core
COPY factories ./factories

COPY main.py .

EXPOSE 8000

CMD [ "poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]