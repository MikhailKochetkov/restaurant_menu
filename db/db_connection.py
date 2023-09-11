import os

from dotenv import load_dotenv

load_dotenv()


CONNECTION_STRING = (f'{os.getenv("PG_DB_URL", default="postgresql")}'
                     f'{os.getenv("POSTGRES_USER", default="postgres")}:'
                     f'{os.getenv("POSTGRES_PASSWORD", default="postgres")}'
                     f'@'
                     f'{os.getenv("DB_HOST", default="localhost")}:'
                     f'{os.getenv("DB_PORT", default=5432)}/'
                     f'{os.getenv("POSTGRES_DB", default="database")}')

TEST_CONNECTION_STRING = ('postgresql+asyncpg://'
                          'postgres:postgres@test-db:5432/test_database')
