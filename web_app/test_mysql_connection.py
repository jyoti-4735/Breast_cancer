import sqlite3

def create_appointments_table():
    try:
        conn = sqlite3.connect("bcd_app.db")  # creates file
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doctor_email TEXT,
                patient_email TEXT,
                date TEXT NOT NULL,
                time TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()

        print("✅ appointments table created successfully!")

    except Exception as e:
        print("❌ Error creating appointments table:", e)


# Run the function
create_appointments_table()