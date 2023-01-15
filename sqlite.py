import sqlite3
from sqlite3 import Error
from datetime import datetime

database = r"sqlite/db/database.db"


def create_connection(db_file):
    """create a database connection to a SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():

    sql_create_berry = """ CREATE TABLE IF NOT EXISTS berry (
                                    userid integer PRIMARY KEY,
                                    lastuse integer,
                                    berrycount integer default 0
                                ); """

    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_berry)
    else:
        print("Error! Cannot create the database connection.")


def add_berries(userid, berrycount):
    sql = """
            INSERT OR IGNORE INTO berry(userid,lastuse,berrycount)
            VALUES(?,?,0);
        """
    sql2 = """
            UPDATE berry SET berrycount = berrycount + ?,
            lastuse = ?
            WHERE userid = ?
        """
    conn = create_connection(database)
    if conn is not None:
        cur = conn.cursor()
        lastuse = datetime.now().timestamp()
        cur.execute(sql, (userid, lastuse))
        cur.execute(sql2, (berrycount, lastuse, userid))
        conn.commit()


def select_berries(userid):
    sql = """
        SELECT *
        FROM berry WHERE userid = ?
        """
    conn = create_connection(database)
    if conn is not None:
        cur = conn.cursor()
        cur.execute(sql, (userid,))
        row = cur.fetchone()
        return row


def leaderboard_berries():
    sql = """
    SELECT userid, berrycount FROM berry ORDER BY berrycount DESC
    """
    conn = create_connection(database)
    if conn is not None:
        cur = conn.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        return results


if __name__ == "__main__":
    main()
