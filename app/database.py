from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from .config import settings

# DATABASE_URL = "postgresql://postgres:raymond@localhost/testdb"
DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()