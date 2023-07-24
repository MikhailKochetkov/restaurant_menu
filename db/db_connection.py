import os
from dotenv import load_dotenv

load_dotenv()


CONNECTION_STRING = (f'{os.getenv("DATABASE_URL", default="sqlite:///")}'
                     f'./{os.getenv("DB_NAME", default="database.db")}')

PG_CONNECTION_STRING = (f'{os.getenv("PG_DB_URL", default="postgresql://")}'
                        f'{os.getenv("PG_USER", default="postgres")}:'
                        f'{os.getenv("PG_PASSWORD", default="postgres")}@'
                        f'{os.getenv("DB_HOST", default="db")}:'
                        f'{os.getenv("DB_PORT", default=5432)}/'
                        f'{os.getenv("PG_DB", default="database")}')
