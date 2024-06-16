from sqlmodel import Session, SQLModel, create_engine
import os


# SQL lite database URL for testing
# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to the database file
relative_path_to_db = os.path.join(current_dir, '../../SweetDreams_db')

# Get the absolute path to the database file
absolute_path_to_db = os.path.abspath(relative_path_to_db)

# Create the SQLite URL
db_url = f'sqlite:///{absolute_path_to_db}'

# Create the engine
connect_args = {"check_same_thread": False}
engine = create_engine(db_url, echo=False, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session
