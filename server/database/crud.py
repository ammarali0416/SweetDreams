from sqlmodel import Session, select

from models.database import BookPlan


def add_bookplan(db: Session, thread_id: str, book_plan: str) -> BookPlan:
    book_plan: BookPlan = BookPlan(Thread_ID=thread_id, Book_Plan=book_plan)
    db.add(book_plan)
    db.commit()
    db.refresh(book_plan)
    return book_plan

def get_bookplan(db: Session, thread_id: str) -> BookPlan:
    return db.exec(select(BookPlan).filter(BookPlan.Thread_ID == thread_id)).first()
    