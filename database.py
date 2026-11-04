import sqlite3

# Connect to database
def connect_db():
    return sqlite3.connect("learning_coach.db")


# Create database table
def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            topic TEXT,
            score INTEGER,
            total INTEGER
        )
    """)

    conn.commit()
    conn.close()


# Save student progress
def save_progress(name, topic, score, total):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO progress
        (student_name, topic, score, total)
        VALUES (?, ?, ?, ?)
    """, (name, topic, score, total))

    conn.commit()
    conn.close()


# Get student progress
def get_progress(name):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM progress WHERE student_name = ?",
        (name,)
    )

    data = cursor.fetchall()
    conn.close()

    return data


# Initialize database
create_table()