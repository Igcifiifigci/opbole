import sqlite3

def init(name):
  return sqlite3.connect(name, check_same_thread=False)

def setup(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS User
            (
                  user_id int,
                  white int,
                  red int,
                  orange int,
                  yellow int,
                  blue int,
                  purple int,
                  black int,
                  wager int ,
                  worth int ,
                  win int ,
                  loss int,
                  vip int

            )
    """)
    conn.commit()
    conn.execute("""CREATE TABLE IF NOT EXISTS title
                    (
                          title TEXT

                    )
            """)
    conn.commit()
    conn.execute("""CREATE TABLE IF NOT EXISTS Club
                    (
                          club1 TEXT,
                          club2 TEXT,
                          club3 TEXT,
                          club4 TEXT

                    )
            """)
    conn.commit()

def add_user(conn, user_id):
  stmt = """INSERT INTO User (user_id, white , red , orange , yellow , blue , purple , black , wager, worth , win , loss , vip)
  VALUES (
  ?,
  100,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  100,
  0,
  0,
  0
)"""
  conn.execute(stmt, (user_id,))
  conn.commit()
  return conn

def get_user_value(conn, user_id: int, items: str):
    stmt = f"SELECT {items} FROM User WHERE user_id={user_id}"
    try:
     r= conn.execute(stmt).fetchone()[0]
    except TypeError:
     r = None
    finally:
     return r

def add_white(conn , user_id : int , white : int):
    stmt = f"UPDATE User SET white = white + ? WHERE user_id =?"
    conn.execute(stmt, (white,user_id))
    conn.commit()

def add_red(conn , user_id : int , white : int):
    stmt = f"UPDATE User SET red = red + ? WHERE user_id =?"
    conn.execute(stmt, (white,user_id))
    conn.commit()

def add_orange(conn , user_id : int , white : int):
    stmt = f"UPDATE User SET orange = orange + ? WHERE user_id =?"
    conn.execute(stmt, (white,user_id))
    conn.commit()

def add_yellow(conn , user_id : int , white : int):
    stmt = f"UPDATE User SET yellow = yellow + ? WHERE user_id =?"
    conn.execute(stmt, (white,user_id))
    conn.commit()

def add_blue(conn , user_id : int , white : int):
    stmt = f"UPDATE User SET blue = blue + ? WHERE user_id =?"
    conn.execute(stmt, (white,user_id))
    conn.commit()

def add_purple(conn , user_id : int , white : int):
    stmt = f"UPDATE User SET purple = purple + ? WHERE user_id =?"
    conn.execute(stmt, (white,user_id))
    conn.commit()

def add_black(conn , user_id : int , white : int):
    stmt = f"UPDATE User SET black = black + ? WHERE user_id =?"
    conn.execute(stmt, (white,user_id))
    conn.commit()
