"""
This file mainly preprocessing and push data from 42_genre_wr_gt_4.csv to postgresql

Author: Pham Thinh 👋
Contact: github.com/Thinh127
"""

from os import replace
from app import db
from app import cleanup
from app.models import *
from app.dto import BookDto
import pandas as pd
import numpy as np
import re

# load data
master_file = pd.read_csv('..\\notebooks\\42_genre_wr_gt_4.csv')

"""

Table AUTHORS

"""

authors_name = master_file['author'].unique()  # get unique name of authors

authors_name = [name.strip() for au in authors_name for name in au.split(
    ',') if re.match(f'\w', str(name))]

authors_name = list(set(authors_name))

authors_list = [Author(full_name=v) for v in authors_name]

db.session.bulk_save_objects(authors_list)
db.session.commit()

"""

Table GENRE

"""

genre_unique = master_file['genre'].unique()

genre = [g.lower() for i in genre_unique for g in str(i).split(',')]
genre = list(set(genre))

list_genre = [Genre(kind=v) for v in genre]
db.session.bulk_save_objects(list_genre)
db.session.commit()

"""

TABLE BOOK_FORMAT

"""

book_format_unique = master_file['bookformat'].unique()

book_format = [str(bf).lower() for bf in book_format_unique
               if re.match(r'\w', str(bf)) and str(bf).lower() != 'nan']

book_format = list(set(book_format))

list_book = [BookFormat(type_=v) for v in book_format]
db.session.bulk_save_objects(list_book)
db.session.commit()

"""

Table BOOK

"""

table_temp = master_file[['isbn', 'isbn13',
                          'title', 'desc', 'pages', 'img', 'link']].copy()

table_temp.columns = ['isbn', 'isbn13', 'title',
                      'desc', 'pages', 'image_url', 'book_url']

list_books = [Book(**BookDto(**dict(table_temp.iloc[i, :])).dict())
              for i in range(table_temp.shape[0])]

db.session.bulk_save_objects(list_books)
db.session.commit()

"""

Table BOOK_REVIEW

"""

book_id = np.arange(1, master_file.shape[0]+1)
book_review = master_file[['rating', 'reviews', 'totalratings']]

book_review.columns = ['rating', 'reviews', 'total_ratings']

book_review.loc[:, 'book_id'] = book_id

book_review_list = [BookReview(**dict(book_review.iloc[i, :]))
                    for i in range(book_review.shape[0])]

db.session.bulk_save_objects(book_review_list)
db.session.commit()

"""

Table BOOK_DETAIL

"""


def getAuthorId(full_name):
    """
    This function receives a author's full_name and return book_id correspond.
    """
    default_id = 'nan'
    global db
    id = [i for i in db.session.query(
        Author.id).filter_by(full_name=full_name).all()]
    if len(id) != 0:
        return id[0][0]
    return default_id


BOOK = master_file[['author']].copy()

# dictionary storing book_id and author_id
BOOK_DETAIL = {'book_id': [],
               'author_id': []}

for idx in range(BOOK.shape[0]):
    list_authors = [author.strip()
                    for author in str(BOOK.iloc[idx, 0]).split(',')
                    if author.lower() != 'nan']
    for au in list_authors:
        au_id = getAuthorId(full_name=au)
        # plus 1 to same to id in database
        BOOK_DETAIL['book_id'].append(idx + 1)
        BOOK_DETAIL['author_id'].append(au_id)

book_id, author_id = BOOK_DETAIL['book_id'], BOOK_DETAIL['author_id']
list_book_detail = [BookDetail(book_id=bo_id, author_id=au_id)
                    for bo_id, au_id in zip(book_id, author_id)]

db.session.bulk_save_objects(list_book_detail)
db.session.commit()

"""

Table BOOK_GENRE

"""


def getGenreId(genre):
    """
    This function receives a book's genre and return genre_id
    """
    default_id = 'nan'
    global db
    id = [i for i in db.session.query(Genre.id).filter_by(kind=genre).all()]
    if len(id) != 0:
        return id[0][0]
    return default_id


BOOK = master_file[['genre']].copy()

# dictionary storing genre_id and book_id
BOOK_GENRE = {'genre_id': [],
              'book_id': []}

for idx in range(BOOK.shape[0]):
    list_genre = [genre.lower().strip()
                  for genre in str(BOOK.iloc[idx, 0]).split(',')
                  if genre.lower() != 'nan']
    for gen in list_genre:
        gen_id = getGenreId(genre=gen)
        BOOK_GENRE['book_id'].append(idx + 1)    # plus 1 to same to id table
        BOOK_GENRE['genre_id'].append(gen_id)

book_id, genre_id = BOOK_GENRE['book_id'], BOOK_GENRE['genre_id']
list_genre = [BookGenre(book_id=bo_id, genre_id=gen_id)
              for bo_id, gen_id in zip(book_id, genre_id)]

db.session.bulk_save_objects(list_genre)
db.session.commit()

"""

Table BOOK_FORMAT_DETAIL

"""


def getFormatId(format):
    """
    This function receives a book's format and return a format_id.
    """
    default_id = 'nan'
    global db
    id = [i for i in db.session.query(
        BookFormat.id).filter_by(type_=format).all()]
    if len(id) != 0:
        return id[0][0]
    return default_id


BOOK = master_file[['bookformat']].copy()

# dictionary storing format_id and book_id
BOOK_FORMAT_DETAIL = {'format_id': [],
                      'book_id': []}

for idx in range(BOOK.shape[0]):
    list_format = [format.lower().strip()
                   for format in str(BOOK.iloc[idx, 0]).split(',')
                   if format.lower() != 'nan']
    for f in list_format:
        f_id = getFormatId(format=f)
        BOOK_FORMAT_DETAIL['book_id'].append(
            idx + 1)    # plus 1 to same to id table
        BOOK_FORMAT_DETAIL['format_id'].append(f_id)

book_id, book_format_id = BOOK_FORMAT_DETAIL['book_id'], BOOK_FORMAT_DETAIL['format_id']
list_format_detail = [BookFormatDetail(
    book_id=bo_id, book_format_id=bo_f_id) for bo_id, bo_f_id in zip(book_id, book_format_id)]

db.session.bulk_save_objects(list_format_detail)
db.session.commit()

"""
Table BOOK_RECOMMEND
"""

recommend = pd.read_json('..\\notebooks\\book_descriptions_recommend_data.json') # json file storing book recommend by book id

BOOK_RECOMMEND = {'book_id': [], 'list_books': []}

for i in range(recommend.shape[0]):
    list_books = recommend.iloc[i, 1]
    for b in list_books:
        BOOK_RECOMMEND['book_id'].append(i+1)
        BOOK_RECOMMEND['list_books'].append(b)

list_book_remmend = [BookDescriptionSimilarities(book_id=bo_id, book_recommend_id=l_bo_id) \
                    for bo_id, l_bo_id in zip(BOOK_RECOMMEND['book_id'], BOOK_RECOMMEND['list_books'])]

db.session.bulk_save_objects(list_book_remmend)
db.session.commit()

# Close connection when done
cleanup(db.session)
