from database.database import engine
from sqlmodel import Session, SQLModel, create_engine
from models.database import BookPlan
from database.crud import add_bookplan, get_bookplan

# Create a test session
def test_get_session():
    with Session(engine) as session:
        assert session is not None
        assert session.is_active is True

        test_book_plan = BookPlan(Thread_ID="test_thread_id", Book_Plan=str({"test_key": "test_value"}))

        session.add(test_book_plan)
        session.commit()

        

def test_get_bookplan():
    res = get_bookplan(db=Session(engine), thread_id="thread_kSKdwqhRIaaZctHVZrYVOcla")
    print(res)
    assert res is not None
    assert res.Thread_ID == "thread_kSKdwqhRIaaZctHVZrYVOcla"
    assert isinstance(res, BookPlan)
    assert isinstance(res.Book_Plan, str)