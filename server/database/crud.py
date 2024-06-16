from sqlmodel import Session, select

from models.database import BookPlan, ChapterOutlines, Chapter, CompletedChapter

from typing import Tuple, List, Dict

import json

import ast

def add_bookplan(db: Session, thread_id: str, book_plan: str) -> BookPlan:
    book_plan: BookPlan = BookPlan(Thread_ID=thread_id, Book_Plan=book_plan)
    db.add(book_plan)
    db.commit()
    db.refresh(book_plan)
    return book_plan

def get_bookplan(db: Session, bookplan_id: int) -> BookPlan:
    return db.exec(select(BookPlan).filter(BookPlan.BookPlan_ID == bookplan_id)).first()

def get_chapter_outlines(db: Session, bookplan_id: int) -> list[ChapterOutlines]:
    return db.exec(select(ChapterOutlines).filter(ChapterOutlines.BookPlan_ID == bookplan_id).order_by(ChapterOutlines.Chapter_Num.asc())).all()

def add_chapter_outlines(db: Session, bookplan_id: int, chapters: list[str]) -> list[ChapterOutlines]:
    for chapter in chapters:
        chapter_json = json.loads(chapter)
        chapter_outline: ChapterOutlines = ChapterOutlines(BookPlan_ID=bookplan_id,
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

    chapter_outlines = get_chapter_outlines(db=db, bookplan_id=bookplan_id)


    return chapter_outlines

def add_chapters(db: Session, chapters: list[Chapter]) -> list[Chapter]:
    for chapter in chapters:
        db.add(chapter)
    db.commit()
    
    for chapter in chapters:
        db.refresh(chapter)
    return chapters

def get_book_elements(db: Session, bookplan_id: int) -> Tuple[List[Dict[str, str]], str]:
    book_plan = db.exec(select(BookPlan).filter(BookPlan.BookPlan_ID == bookplan_id)).first()
    title = ast.literal_eval(book_plan.Book_Plan)['bookPlan']['title']
    chapters = book_plan.Chapters
    chapter_outlines = book_plan.Chapter_Outlines

    completed_chapters = [
        CompletedChapter(
            Number=outline.Chapter_Num,
            Title=outline.Chapter,
            Content=chapter.Chapter
        )
        for outline in chapter_outlines
        for chapter in chapters
        if outline.Chapter_Num == chapter.Chapter_Num
    ]

    return completed_chapters, title

def get_illustration_context(db: Session, bookplan_id: int) -> Tuple[str, str, List[Tuple[int, str, str]]]:
    book_plan: BookPlan = get_bookplan(db=db, bookplan_id=bookplan_id)
    book_plan_dict: dict = ast.literal_eval(book_plan.Book_Plan)
    illustrative_style: str = book_plan_dict['bookPlan']['illustrativeStyle']
    main_characters: str = str(book_plan_dict['bookPlan']['mainCharacters'])

    chapter_outlines: List[ChapterOutlines] = get_chapter_outlines(db=db, bookplan_id=bookplan_id)
    
    chapter_details: List[Tuple[int, str, str]] = [
        (outline.Chapter_Num, outline.PlotDevelopment, outline.IllustrationIdeas)
        for outline in chapter_outlines
    ]

    return illustrative_style, main_characters, chapter_details

