import os
import time
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "mysql"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

if not all(DB_CONFIG.values()):
    raise Exception("Missing DB environment variables: " +
                    str([k for k, v in DB_CONFIG.items() if not v]))


def get_db_connection(retries=10, delay=3):
    last_err = None
    for attempt in range(retries):
        try:
            return mysql.connector.connect(**DB_CONFIG)
        except mysql.connector.Error as e:
            last_err = e
            time.sleep(delay)
    raise Exception(f"Database connection failed after {retries} attempts: {last_err}")


@app.route("/health")
def health():
    try:
        conn = get_db_connection(retries=1, delay=0)
        conn.close()
        return {"status": "ok"}
    except Exception:
        return {"status": "db_unavailable"}, 503


@app.route("/")
def index():
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, message_text,
            DATE_FORMAT(created_at,'%H:%i:%s') AS time
            FROM user_messages
            ORDER BY id DESC
        """)
        messages = cursor.fetchall()
        cursor.close()
    finally:
        conn.close()          # ← always close even on exception
    return render_template("dashboard.html", saved_messages=messages)


@app.route("/add", methods=["POST"])
def add():
    msg = request.form.get("user_text", "").strip()
    if msg:
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user_messages(message_text) VALUES(%s)", (msg,)
            )
            conn.commit()
            cursor.close()
        finally:
            conn.close()
    return redirect(url_for("index"))