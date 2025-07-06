# coding=utf-8
""""
Class for interacting with the database
"""
import sqlite3
from config import DATABASE_PATH


class DBManager:
    def __init__(self, database):
        self.database = database
    
    
    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS "scripts" (
                            "script_id"   INTEGER NOT NULL UNIQUE,
                            "name"        TEXT NOT NULL,
                            "user_id"     INTEGER NOT NULL,
                            "description" TEXT,
                            "script"      TEXT NOT NULL,
                            "likes"       INTEGER NOT NULL DEFAULT 0,
                            PRIMARY KEY("script_id" AUTOINCREMENT));''')
            
            conn.execute('''CREATE TABLE IF NOT EXISTS "users" (
                            "id"            INTEGER NOT NULL UNIQUE,
                            "username"      TEXT NOT NULL UNIQUE,
                            "scripts_count" INTEGER NOT NULL DEFAULT 0,
                            PRIMARY KEY("id" AUTOINCREMENT));''')
            conn.commit()
    
    
    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()
    
    
    def __select_data(self, sql, data=tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()
    
    
    def get_script_data(self, script_id):
        return self.__select_data("SELECT script FROM scripts WHERE script_id = ?", (script_id,))[0][0]
    
    
    def get_script_name(self, script_id):
        return self.__select_data("SELECT name FROM scripts WHERE script_id = ?", (script_id,))[0][0]
    
    
    def get_script_description(self, script_id):
        return self.__select_data("SELECT description FROM scripts WHERE script_id = ?", (script_id,))[0][0]
    
    
    def get_script_creator(self, script_id):
        return self.__select_data("""SELECT username FROM scripts
                                         INNER JOIN users ON users.id = scripts.user_id
                                         WHERE script_id = ?""", (script_id,))[0][0]
    
    
    def get_user_scripts(self, user_id):
        return [item[0] for item in self.__select_data("""SELECT script_id FROM scripts
                                                              INNER JOIN users ON users.id = scripts.user_id
                                                              WHERE users.id = ?""", (user_id,))]
    
    
    def get_users_rating(self):
        return self.__select_data("""SELECT username, SUM(likes) AS total_likes
                                     FROM scripts
                                     INNER JOIN users ON users.id = scripts.user_id
                                     GROUP BY user_id
                                     ORDER BY total_likes DESC
                                     LIMIT 10""")
    
    
    def get_scripts_rating(self):
        return self.__select_data("""SELECT name, likes FROM scripts
                                        ORDER BY likes DESC""")
    
    
    def get_user_id(self, username):
        return self.__select_data("SELECT id FROM users WHERE username = ?", (username,))[0][0]
    
    
    def get_script_id_by_name(self, script_name):
        return [item[0] for item in self.__select_data("SELECT script_id FROM scripts WHERE name = ?", (script_name,))]
    
    
    def add_script(self, name, data, user_id, description=""):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO scripts(name, user_id, description, script) VALUES (?, ?, ?, ?)", (name, user_id, description, data))
            conn.commit()
    
    
    def register_user(self, username):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT username FROM users WHERE username = ?", (username,))
            res = cur.fetchone()
            if not res:
                cur.execute("INSERT INTO users(username) VALUES (?)", (username,))
            conn.commit()


if __name__ == '__main__':
    manager = DBManager(DATABASE_PATH)
    manager.create_tables()
    print(manager.get_script_data(1))
    print(manager.get_script_name(1))
    print(manager.get_script_description(1))
    print(manager.get_script_creator(1))
    print(manager.get_user_scripts(1))
    print(manager.get_users_rating())
    print(manager.get_scripts_rating())
    print(manager.get_user_id("Tema"))
    print(manager.get_script_id_by_name("Test1"))
