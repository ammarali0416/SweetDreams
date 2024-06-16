from database.database import engine
from sqlmodel import Session, SQLModel, create_engine, select
from models.database import BookPlan
from database.crud import add_bookplan, get_bookplan, get_book_elements, get_illustration_context
import ast

# Create a test session
def test_get_session():
    with Session(engine) as session:
        assert session is not None
        assert session.is_active is True

        #test_book_plan = BookPlan(Thread_ID="test_thread_id", Book_Plan=str({"test_key": "test_value"}))

        #session.add(test_book_plan)
        #session.commit()

        

def test_get_bookplan():
    res = get_bookplan(db=Session(engine), bookplan_id=12)
    #print(res)
    assert res is not None
    assert isinstance(res, BookPlan)
    import ast

    res = ast.literal_eval(res.Book_Plan)

    with Session(engine) as db:
        res = db.exec(select(BookPlan).filter(BookPlan.BookPlan_ID == 12)).first()
        res = ast.literal_eval(res.Book_Plan)
        assert res is not None
        assert isinstance(res, dict)



def test_get_book_elements():
    db = Session(engine)
    bookplan_id = 12
    combined_list, title = get_book_elements(db=db, bookplan_id=bookplan_id)

    assert combined_list is not None
    assert title is not None
    assert title == "The Magic of Luna's Garden"

    # Print the output for verification
    #print("Title:", title)
    #for entry in combined_list:
        #print(f"Number: {entry.Number}, Title: {entry.Title}, Content: {entry.Content}")

def test_get_illustration_context():
    db = Session(engine)
    bookplan_id = 12 

    overall_style, characters, chapter_details = get_illustration_context(db=db, bookplan_id=bookplan_id)

    assert overall_style is not None
    assert characters is not None
    assert chapter_details is not None

    # Print the output for verification
    #print("Overall Style:", overall_style)
    #print("Characters:", characters)
    #for chapter in chapter_details:
    #    print(f"Chapter Number: {chapter[0]}, Plot Development: {chapter[1]}, Illustration Ideas: {chapter[2]}")