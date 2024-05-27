from database.database import engine, create_db_and_tables
from sqlmodel import Session, SQLModel, create_engine
from models.database import BookPlan

# Create a test session
def test_get_session():
    create_db_and_tables()
    with Session(engine) as session:
        assert session is not None
        assert session.is_active is True

        test_book_plan = BookPlan(Thread_ID="test_thread_id", Book_Plan=str({"test_key": "test_value"}))

        session.add(test_book_plan)
        session.commit()

        

