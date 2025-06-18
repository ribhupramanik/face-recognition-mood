import sqlite3

def create_table_if_not_exists():
    conn = sqlite3.connect("database.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS STUDENTS (
            ID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            Age INTEGER NOT NULL
        );
    """)
    conn.commit()
    conn.close()

def insert_or_update(Id, Name, Age):
    create_table_if_not_exists()  # Ensure table exists first

    conn = sqlite3.connect("database.db")
    cursor = conn.execute("SELECT * FROM STUDENTS WHERE ID=?", (Id,))
    record = cursor.fetchone()

    if record:
        conn.execute("UPDATE STUDENTS SET Name=?, Age=? WHERE ID=?", (Name, Age, Id))
    else:
        conn.execute("INSERT INTO STUDENTS (ID, Name, Age) VALUES (?, ?, ?)", (Id, Name, Age))

    conn.commit()
    conn.close()
