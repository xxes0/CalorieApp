# database.py
import os
import sqlite3
from datetime import datetime
from contextlib import closing

DB_DIR = os.environ.get("CALORIE_DB_DIR",
                        os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(DB_DIR, "calorie.db")


def _connect():
    return sqlite3.connect(DB_PATH)


def init_db():
    with closing(_connect()) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL, gender TEXT NOT NULL, age INTEGER NOT NULL,
                weight REAL NOT NULL, height REAL NOT NULL,
                activity TEXT NOT NULL, goal TEXT NOT NULL, target INTEGER NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS photo_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL, photo_path TEXT NOT NULL,
                recognized TEXT NOT NULL, matched TEXT,
                grams INTEGER NOT NULL, kcal_total INTEGER NOT NULL
            )
        """)
        conn.commit()


def save_record(gender, age, weight, height, activity, goal, target):
    with closing(_connect()) as conn:
        conn.execute(
            "INSERT INTO history (date, gender, age, weight, height, activity, goal, target) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (datetime.now().strftime("%Y-%m-%d %H:%M"),
             gender, int(age), float(weight), float(height),
             activity, goal, int(target)))
        conn.commit()


def get_history(limit=50):
    with closing(_connect()) as conn:
        cur = conn.execute(
            "SELECT date, gender, age, weight, height, activity, goal, target "
            "FROM history ORDER BY id DESC LIMIT ?", (limit,))
        return cur.fetchall()


def save_photo_record(photo_path, recognized, matched, grams, kcal_total):
    with closing(_connect()) as conn:
        conn.execute(
            "INSERT INTO photo_history (date, photo_path, recognized, matched, grams, kcal_total) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (datetime.now().strftime("%Y-%m-%d %H:%M"),
             photo_path, recognized, matched or "—", int(grams), int(kcal_total)))
        conn.commit()


def get_photo_history(limit=50):
    """Возвращает: date, photo_path, recognized, grams, kcal_total"""
    with closing(_connect()) as conn:
        cur = conn.execute(
            "SELECT date, photo_path, recognized, grams, kcal_total "
            "FROM photo_history ORDER BY id DESC LIMIT ?", (limit,))
        return cur.fetchall()