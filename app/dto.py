"""
In this file, classes using for constraint data type. (Handle error: can't adapt numpyint64)

Author: Pham Thinh 👋
Contact: github.com/Thinh127
"""

from pydantic import BaseModel


class BookDto(BaseModel):
    isbn: str = None
    isbn13: str = None
    title: str = None
    desc: str = None
    pages: int = None
    image_url: str = None
    book_url: str = None


class BookReview(BaseModel):
    rating: float = None
    reviews: int = None
    total_ratings: int = None
    book_id: int = None
