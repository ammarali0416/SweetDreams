from sqlmodel import Session

from models.database import BookPlan


def add_bookplan(db: Session, thread_id: str, book_plan: str):
    book_plan = BookPlan(Thread_ID=thread_id, Book_Plan=book_plan)
    db.add(book_plan)
    db.commit()
    db.refresh(book_plan)
    return book_plan