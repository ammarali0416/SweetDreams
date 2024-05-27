from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

class BookPlan(SQLModel, table=True):
    BookPlan_ID: Optional[int] = Field(default=None, primary_key=True)
    Thread_ID: str
    Book_Plan: str