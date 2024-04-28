import datetime
import sqlite3

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'tgids'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True, unique=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    def __repr__(self):
        return f'<User> {self.id} {self.created_date}'
