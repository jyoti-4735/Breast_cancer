import sqlite3

# 🔹 Connect to database
def connect_to_db():
    return sqlite3.connect("bcd_app.db")


# 🔹 Create Patients Table
def create_patients_table():
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        phone TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


# 🔹 Create Doctors Table
def create_doctors_table():
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        phone TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


# 🔹 Create Appointments Table
def create_appointments_table():
    conn = connect_to_db()
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


# 🔹 Insert Patient
def insert_patient(name, email, phone, password):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO patients (name, email, phone, password) VALUES (?, ?, ?, ?)",
            (name, email, phone, password)
        )
        conn.commit()
    except Exception as e:
        print("❌ Error inserting patient:", e)

    conn.close()


# 🔹 Insert Doctor
def insert_doctor(name, email, phone, password):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO doctors (name, email, phone, password) VALUES (?, ?, ?, ?)",
            (name, email, phone, password)
        )
        conn.commit()
    except Exception as e:
        print("❌ Error inserting doctor:", e)

    conn.close()


# 🔹 Validate User (Login)
def validate_user(email, password, role="patient"):
    conn = connect_to_db()
    cursor = conn.cursor()

    if role == "doctor":
        cursor.execute(
            "SELECT * FROM doctors WHERE email=? AND password=?",
            (email, password)
        )
    else:
        cursor.execute(
            "SELECT * FROM patients WHERE email=? AND password=?",
            (email, password)
        )

    user = cursor.fetchone()
    conn.close()

    return user


# 🔹 Initialize all tables
def init_db():
    create_patients_table()
    create_doctors_table()
    create_appointments_table()


# 🔹 Run once when file is executed
if __name__ == "__main__":
    init_db()
    print("✅ Database setup complete!")