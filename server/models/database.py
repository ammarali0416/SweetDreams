from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel
from pydantic import BaseModel

class BookPlan(SQLModel, table=True):
    BookPlan_ID: Optional[int] = Field(default=None, primary_key=True)
    Thread_ID: str
    Book_Plan: str

    Chapter_Outlines: List["ChapterOutlines"] | None = Relationship(back_populates="Book_Plan")
    Chapters: List["Chapter"] | None = Relationship(back_populates="Book_Plan")

class ChapterOutlines(SQLModel, table=True):
    ChapterOutline_ID: Optional[int] = Field(default=None, primary_key=True)
    BookPlan_ID: int = Field(foreign_key="bookplan.BookPlan_ID")
    Chapter_Outline_JSON: str
    Chapter_Num: int
    Chapter: str
    EstimatedWordCount: int
    Setting: str
    MainCharacters: str
    PlotDevelopment: str
    IllustrationIdeas: str
    WritingStyleNuances: str
    ThemesAndMessages: str

    Book_Plan: BookPlan = Relationship(back_populates="Chapter_Outlines")
    Chapter_written: List["Chapter"] | None = Relationship(back_populates="ChapterOutline")

class Chapter(SQLModel, table=True):
    Chapter_ID: Optional[int] = Field(default=None, primary_key=True)
    ChapterOutline_ID: int = Field(foreign_key="chapteroutlines.ChapterOutline_ID")
    BookPlan_ID: int = Field(foreign_key="bookplan.BookPlan_ID")
    Chapter_Num: int
    Chapter: str

    ChapterOutline: ChapterOutlines = Relationship(back_populates="Chapter_written")
    Book_Plan: BookPlan = Relationship(back_populates="Chapters")

class CompletedChapter(BaseModel):
    Number: int
    Title: str
    Content: str
