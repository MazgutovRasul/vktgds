import datetime
import sqlite3

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    db = 'userids.db'
    con = sqlite3.connect(db)
    cur = con.cursor()
    vkids = dict(cur.execute("""SELECT * FROM vkids""").fetchall())
    __tablename__ = 'vkids'
    id = ''
    for el in vkids:
        id = el + 1
    if id == '':
        id = 1
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, default=id)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    def __repr__(self):
        return f'<User> {self.id} {self.created_date}'
