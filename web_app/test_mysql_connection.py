import mysql.connector
from mysql.connector import Error

config = {
    "host": "localhost",
    "user": "bcd_user",
    "password": "jyoti.k@4735",
    "database": "bcd_app",
    "auth_plugin": "caching_sha2_password"
}

def create_appointments_table():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                doctor_email VARCHAR(100),
                patient_email VARCHAR(100),
                date DATE NOT NULL,
                time TIME NOT NULL
            )
        """)
        conn.commit()
        conn.close()
        print("✅ appointments table created successfully!")
    except Error as e:
        print("❌ Error creating appointments table:", e)

# Run the function
create_appointments_table()
