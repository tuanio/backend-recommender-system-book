"""
This file mainly preprocessing and push data from 42_genre_wr_gt_4.csv to postgresql

Author: Pham Thinh 👋
Contact: github.com/Thinh127
"""

import os
import re
from app import db
import numpy as np
import pandas as pd
from app.models import *
from app.dto import BookDto
from app.utils import cleanup, write
import concurrent.futures as cf

cwd = ""

# load data
master_file = pd.read_csv(cwd + "notebooks/50_genre_800_author_wr_gt_4.csv")

write("Table AUTHORS")

authors_name = master_file["author"].unique()  # get unique name of authors

authors_name = [
    name.strip()
    for au in authors_name
    for name in au.split(",")
    if re.match(f"\w", str(name))
]

authors_name = set(authors_name)

with cf.ThreadPoolExecutor() as executor:
    authors_list = list(executor.map(lambda v: Author(full_name=v), authors_name))

db.session.bulk_save_objects(authors_list)
db.session.commit()

write("Table GENRE")

genre_unique = master_file["genre"].unique()

genre = [g for i in genre_unique for g in str(i).split(",")]
genre = set(genre)

with cf.ThreadPoolExecutor() as executor:
    list_genre = list(executor.map(lambda v: Genre(kind=v), genre))

db.session.bulk_save_objects(list_genre)
db.session.commit()

write("TABLE BOOK_FORMAT")

book_format_unique = master_file["bookformat"].unique()

book_format = [
    str(bf)
    for bf in book_format_unique
    if re.match(r"\w", str(bf)) and str(bf) != "nan"
]

book_format = set(book_format)

with cf.ThreadPoolExecutor() as executor:
    list_book = list(executor.map(lambda v: BookFormat(type_=v), book_format))
db.session.bulk_save_objects(list_book)
db.session.commit()

write("Table BOOK")

table_temp = master_file[
    ["isbn", "isbn13", "title", "desc", "pages", "img", "link"]
].copy()

table_temp.columns = [
    "isbn",
    "isbn13",
    "title",
    "desc",
    "pages",
    "image_url",
    "book_url",
]

with cf.ThreadPoolExecutor() as executor:
    list_books = list(
        executor.map(
            lambda i: Book(**BookDto(**dict(table_temp.iloc[i, :])).dict()),
            range(table_temp.shape[0]),
        )
    )

db.session.bulk_save_objects(list_books)
db.session.commit()

write("Table BOOK_REVIEW")

book_id = np.arange(1, master_file.shape[0] + 1)
book_review = master_file[["rating", "reviews", "totalratings", "weighted_rating"]]

book_review.columns = ["rating", "reviews", "total_ratings", "weighted_rating"]

book_review.loc[:, "book_id"] = book_id

with cf.ThreadPoolExecutor() as executor:
    book_review_list = list(
        executor.map(
            lambda i: BookReview(**dict(book_review.iloc[i, :])),
            range(book_review.shape[0]),
        )
    )

db.session.bulk_save_objects(book_review_list)
db.session.commit()

write("Table BOOK_DETAIL")


def getAuthorId(full_name):
    """
    This function receives a author's full_name and return book_id correspond.
    """
    default_id = "nan"
    # global db
    # id = [i for i in db.session.query(Author.id).filter_by(full_name=full_name).all()]
    id_ = db.session.query(Author.id).filter_by(full_name=full_name).first()
    if id_:
        return id_[0]
    return default_id


BOOK = master_file[["author"]].copy()

# dictionary storing book_id and author_id
BOOK_DETAIL = {"book_id": [], "author_id": []}

for idx in range(BOOK.shape[0]):
    list_authors = [
        author.strip()
        for author in str(BOOK.iloc[idx, 0]).split(",")
        if author != "nan"
    ]
    for au in list_authors:
        au_id = getAuthorId(full_name=au)
        # plus 1 to same to id in database
        BOOK_DETAIL["book_id"].append(idx + 1)
        BOOK_DETAIL["author_id"].append(au_id)

book_id, author_id = BOOK_DETAIL["book_id"], BOOK_DETAIL["author_id"]
list_book_detail = [
    BookDetail(book_id=bo_id, author_id=au_id)
    for bo_id, au_id in zip(book_id, author_id)
]

db.session.bulk_save_objects(list_book_detail)
db.session.commit()

write("Table BOOK_GENRE")


def getGenreId(genre):
    """
    This function receives a book's genre and return genre_id
    """
    default_id = "nan"
    # global db
    # id = [i for i in db.session.query(Genre.id).filter_by(kind=genre).all()]
    id_ = db.session.query(Genre.id).filter_by(kind=genre).first()
    if id_:
        return id_[0]
    return default_id


BOOK = master_file[["genre"]].copy()

# dictionary storing genre_id and book_id
BOOK_GENRE = {"genre_id": [], "book_id": []}

for idx in range(BOOK.shape[0]):
    list_genre = [
        genre.strip() for genre in str(BOOK.iloc[idx, 0]).split(",") if genre != "nan"
    ]
    for gen in list_genre:
        gen_id = getGenreId(genre=gen)
        BOOK_GENRE["book_id"].append(idx + 1)  # plus 1 to same to id table
        BOOK_GENRE["genre_id"].append(gen_id)

book_id, genre_id = BOOK_GENRE["book_id"], BOOK_GENRE["genre_id"]
list_genre = [
    BookGenre(book_id=bo_id, genre_id=gen_id)
    for bo_id, gen_id in zip(book_id, genre_id)
]

db.session.bulk_save_objects(list_genre)
db.session.commit()

write("Table BOOK_FORMAT_DETAIL")


def getFormatId(format):
    """
    This function receives a book's format and return a format_id.
    """
    default_id = "nan"
    # global db
    # id = [i for i in db.session.query(
    #     BookFormat.id).filter_by(type_=format).all()]
    id_ = db.session.query(BookFormat.id).filter_by(type_=format).first()
    if id_:
        return id_[0]
    return default_id


BOOK = master_file[["bookformat"]].copy()

# dictionary storing format_id and book_id
BOOK_FORMAT_DETAIL = {"format_id": [], "book_id": []}

for idx in range(BOOK.shape[0]):
    list_format = [
        format.strip()
        for format in str(BOOK.iloc[idx, 0]).split(",")
        if format != "nan"
    ]
    for f in list_format:
        f_id = getFormatId(format=f)
        BOOK_FORMAT_DETAIL["book_id"].append(idx + 1)  # plus 1 to same to id table
        BOOK_FORMAT_DETAIL["format_id"].append(f_id)

book_id, book_format_id = BOOK_FORMAT_DETAIL["book_id"], BOOK_FORMAT_DETAIL["format_id"]
list_format_detail = [
    BookFormatDetail(book_id=bo_id, book_format_id=bo_f_id)
    for bo_id, bo_f_id in zip(book_id, book_format_id)
]

db.session.bulk_save_objects(list_format_detail)
db.session.commit()

write("Table BOOK_RECOMMEND")

recommend = pd.read_json(
    cwd + "notebooks/book_descriptions_recommend_data.json"
)  # json file storing book recommend by book id

BOOK_RECOMMEND = {"book_id": [], "list_books": []}

for i in range(recommend.shape[0]):
    list_books = recommend.iloc[i, 1]
    for b in list_books:
        BOOK_RECOMMEND["book_id"].append(i + 1)
        BOOK_RECOMMEND["list_books"].append(b)

list_book_remmend = [
    BookDescriptionSimilarities(book_id=bo_id, book_recommend_id=l_bo_id)
    for bo_id, l_bo_id in zip(BOOK_RECOMMEND["book_id"], BOOK_RECOMMEND["list_books"])
]

db.session.bulk_save_objects(list_book_remmend)
db.session.commit()


# Close connection when done
cleanup(db.session)
