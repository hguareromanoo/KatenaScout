# backend/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.config import DATABASE_URL
from backend.models.sql_models import Base # Assuming Base is defined in sql_models

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Provides a database session for a single request.
    Ensures the session is closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initializes the database by creating all tables defined in the models.
    This function should be called explicitly during application setup or
    via a separate script, not typically during each application run.
    """
    # Import all modules here that might define models so they are
    # registered properly on the metadata. Otherwise, you will have to
    # import them first before calling init_db().
    # For this project, all models are in backend.models.sql_models
    # which is already imported for Base.
    print(f"Initializing database at {DATABASE_URL}...")
    Base.metadata.create_all(bind=engine)
    print("Database initialization complete. Tables created (if they didn't exist).")

# Example of how to use init_db (e.g., in a setup script):
# if __name__ == "__main__":
#     print("This script is for setting up the database.")
#     # Consider adding checks or confirmations before running,
#     # as create_all is non-destructive for existing tables but
#     # this script might be run inadvertently.
#     init_db()
