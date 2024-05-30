from sqlmodel import Session, select

from models.database import BookPlan, ChapterOutlines

import json


def add_bookplan(db: Session, thread_id: str, book_plan: str) -> BookPlan:
    book_plan: BookPlan = BookPlan(Thread_ID=thread_id, Book_Plan=book_plan)
    db.add(book_plan)
    db.commit()
    db.refresh(book_plan)
    return book_plan

def get_bookplan(db: Session, thread_id: str) -> None:
    return db.exec(select(BookPlan).filter(BookPlan.Thread_ID == thread_id)).first()

def add_chapters(db: Session, thread_id: str, chapters: list[str]) -> list[ChapterOutlines]:
    for chapter in chapters:
        chapter_json = json.loads(chapter)
        chapter_outline: ChapterOutlines = ChapterOutlines(Thread_ID=thread_id,
                                                           Chapter_Outline_JSON=chapter,
                                                           Chapter_Num=chapter_json['Index'],
                                                           Chapter=chapter_json['Chapter'],
                                                           EstimatedWordCount=chapter_json['EstimatedWordCount'],
                                                           Setting=chapter_json['Setting'],
                                                           MainCharacters=chapter_json['MainCharacters'],
                                                           PlotDevelopment=chapter_json['PlotDevelopment'],
                                                           IllustrationIdeas=chapter_json['IllustrationIdeas'],
                                                           WritingStyleNuances=chapter_json['WritingStyleNuances'],
                                                           ThemesAndMessages=chapter_json['ThemesAndMessages'])
        db.add(chapter_outline)
    db.commit()

    chapter_outlines = db.exec(select(ChapterOutlines).filter(ChapterOutlines.Thread_ID == thread_id).order_by(ChapterOutlines.Chapter_Num.asc())).all()


    return chapter_outlines
    