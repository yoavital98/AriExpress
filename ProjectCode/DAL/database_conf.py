from peewee import PostgresqlDatabase, SqliteDatabase


class DatabaseConf:

    # database = SqliteDatabase('database.db')
    database = PostgresqlDatabase('postgres', user='postgres', password='lilythecat',
                                       host='database-1.ckwkbfc5249a.eu-north-1.rds.amazonaws.com', port=5432)