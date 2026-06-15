import os
import time
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ----------------------------
# DB CONFIG
# ----------------------------
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "mysql"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

# Validate env variables early
missing_vars = [k for k, v in DB_CONFIG.items() if not v]
if missing_vars:
    raise Exception(f"Missing DB environment variables: {missing_vars}")

# DB CONNECTION WITH RETRY
def get_db_connection(retries=10, delay=3):
    last_err = None

    for _ in range(retries):
        try:
            return mysql.connector.connect(**DB_CONFIG)
        except mysql.connector.Error as e:
            last_err = e
            time.sleep(delay)

    raise Exception(f"Database connection failed: {last_err}")

# AUTO DB INITIALIZATION
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            message_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()


# Run DB init at startup
init_db()



# HEALTH CHECK
@app.route("/health")
def health():
    try:
        conn = get_db_connection(retries=1, delay=0)
        conn.close()
        return {"status": "ok"}
    except Exception:
        return {"status": "db_unavailable"}, 503


# HOME PAGE
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

    except Exception as e:
        return f"Database error: {str(e)}", 500

    finally:
        cursor.close()
        conn.close()

    return render_template("dashboard.html", saved_messages=messages)


# ADD MESSAGE
@app.route("/add", methods=["POST"])
def add():
    msg = request.form.get("user_text", "").strip()

    if msg:
        conn = get_db_connection()
        try:
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO user_messages(message_text) VALUES(%s)",
                (msg,)
            )

            conn.commit()

        finally:
            cursor.close()
            conn.close()

    return redirect(url_for("index"))

# RUN LOCALLY (optional)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)