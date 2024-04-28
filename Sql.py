import sqlite3

db = sqlite3.connect("main.db")
cursor = db.cursor()

# cursor.execute("""CREATE TABLE users(
#     id integer
# )""")
#
# cursor.execute("""CREATE TABLE users_name(
#     id integer,
#     name text
# )""")

def insert_in_user(user_id):
    value = cursor.execute("""SELECT * FROM users WHERE id = (?)""", (user_id,))
    value = cursor.fetchone()
    print(value)
    if value:
        return 'Вы уже были подписаны'
    else:
        cursor.execute("""INSERT INTO users (id) VALUES (?)""", (user_id,))
        db.commit()
        return 'Вы успешно подписались'


def insert_in_user_name(user_id, user_name):
    value = cursor.execute("""SELECT * FROM users_name WHERE id = (?)""", (user_id,))
    value = cursor.fetchone()
    if value:
        cursor.execute("""UPDATE users_name SET name = ? WHERE id = ?""", (user_name, user_id,))
        db.commit()
    else:
        cursor.execute("""INSERT INTO users_name (id, name) VALUES (?, ?)""", (user_id, user_name,))
        db.commit()

def select_all_from_users():
    value = cursor.execute("""SELECT * FROM users """)
    value = cursor.fetchall()
    return value

def select_all_from_users_name():
    value = cursor.execute("""SELECT * FROM users_name """)
    value = cursor.fetchall()
    return value

def search_id_in_users(user_id):
    for i in select_all_from_users():
        if user_id == i[0]:
            return True

def search_id_in_users_name(user_id):
    for i in select_all_from_users_name():
        if user_id == i[0]:
            return i[1]

