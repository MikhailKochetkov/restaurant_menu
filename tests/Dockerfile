FROM python:3.8-alpine

WORKDIR /tests

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir pytest pytest_asyncio asyncio httpx fastapi

COPY . /tests

CMD ["pytest"]