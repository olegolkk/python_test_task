import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DB_URL = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_DB_HOST')}:{os.getenv('POSTGRES_DB_PORT')}"

engine = create_engine(DB_URL)

try:
    with engine.connect() as conn:
        print("✅ Подключение успешно!")
except Exception as e:
    print(f"❌ Ошибка: {e}")

Session = sessionmaker(engine)

def get_db_session() -> Session:
    return Session