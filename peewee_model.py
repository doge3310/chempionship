from peewee import MySQLDatabase, Model, AutoField, CharField, ForeignKeyField, DateTimeField
from pymysql import MySQLError
from hasher import hash
from datetime import datetime
import pymysql

# Defines
DB_HOST = 'localhost'
DB_PORT     = 3306
DB_USERNAME = 'root'
DB_PASSWORD = '192837465DOge'
DB_NAME     = 'users_1'

def init_database():
    '''Creating database if it does not exists'''
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USERNAME,
            password=DB_PASSWORD
        )

        with connection.cursor() as cursor:
            cursor.execute(f'CREATE DATABASE IF NOT EXISTS {DB_NAME}')

        print(f'Database {DB_NAME} is initialized!')
    except MySQLError as e:
        print(f"Error creating database: {e}")
    finally:
        if 'connection' in locals() and connection:
            connection.close()


init_database()

# Creating connection
db_connection = MySQLDatabase(
    DB_NAME,
    user=DB_USERNAME,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)


class Table(Model):
    id = AutoField()

    class Meta:
        database = db_connection


class Roles(Table):
    name = CharField()


class User(Table):
    username = CharField(unique=1)
    password = CharField()
    role_id = ForeignKeyField(Roles)


class News(Table):
    name = CharField()
    author = CharField()
    content = CharField()
    date_added = DateTimeField(default=datetime.now().isoformat())


class Comments(Table):
    name = CharField()
    new_id = ForeignKeyField(News, backref="news_id")
    content = CharField()
    date_added = DateTimeField(default=datetime.now().isoformat())


@db_connection.atomic()
def main():
    user_role, _ = Roles.get_or_create(name="user")

    base_new, _ = News.get_or_create(name="1",
                                     defaults={
                                         "author": "2",
                                         "content": "1",
                                     })

    base_comment, _ = Comments.get_or_create(name="3",
                                             defaults={
                                                 "content": "3",
                                                 "new": base_new
                                             })

    base_user, _ = User.get_or_create(username="penis_2",
                                      defaults={
                                          "password": hash("1234"),
                                          "role_id": user_role
                                      })


if __name__ == "__main__":
    db_connection.create_tables([User, Roles, News, Comments])

    main()
