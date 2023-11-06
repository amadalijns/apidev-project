from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Verbinden met de SQLite-database
SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlitedb/sqlitedata.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# De engine aanmaken
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Een sessie maken die wordt gebruikt om te communiceren met de database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declaratieve basis voor de database
Base = declarative_base()
