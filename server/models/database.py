from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

class BookPlan(SQLModel, table=True):
    BookPlan_ID: Optional[int] = Field(default=None, primary_key=True)
    Thread_ID: str
    Book_Plan: str

class ChapterOutlines(SQLModel, table=True):
    ChapterOutline_ID: Optional[int] = Field(default=None, primary_key=True)
    Thread_ID: str
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