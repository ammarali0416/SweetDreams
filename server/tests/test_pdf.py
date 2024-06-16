from pdf.pdf import PDF
from models.database import CompletedChapter
from database.crud import get_book_elements
from database.database import engine

from sqlmodel import Session, SQLModel, create_engine, select

def test_pdf():
    with Session(engine) as db:
        bookplan_id = 12
        combined_list, title = get_book_elements(db=db, bookplan_id=bookplan_id)
        chapters = [CompletedChapter(**entry.dict()) for entry in combined_list]
        pdf = PDF(title=title, chapters=chapters)
        pdf.generate_pdf()
        pdf.save_pdf("test.pdf")
        assert True
