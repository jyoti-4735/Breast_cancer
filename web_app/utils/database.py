#!/usr/bin/env python

import mysql.connector
from mysql.connector import Error

# MySQL DB configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "bcd_user",
    "password": "jyoti.k@4735",       # 🔁 change this to your real MySQL password
    "database": "bcd_app",
    
}

def connect_to_db():
    return mysql.connector.connect(**DB_CONFIG)

# ------------------ Initialization ------------------

def init_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS doctors (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                qualification TEXT,
                specialization TEXT,
                experience INT,
                password VARCHAR(100) NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(20),
                password VARCHAR(100) NOT NULL
            )
        """)

        conn.commit()
        conn.close()
    except Error as e:
        print("DB Init Error:", e)

def create_appointments_table():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
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
    except Error as e:
        print("Appointments Table Error:", e)

# ------------------ Insertions ------------------

def insert_patient(name, email, phone, password):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        query = "INSERT INTO patients (name, email, phone, password) VALUES (%s, %s, %s, %s)"
        print("Running query:", query % (name, email, phone, password))  # Debug
        cursor.execute(query, (name, email, phone, password))
        conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        print("Insert patient error:", err)
        raise

def insert_doctor(name, email, qualification, specialization, experience, password):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        query = "INSERT INTO doctors (name, email, qualification, specialization, experience, password) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (name, email, qualification, specialization, experience, password))
        conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        print("Insert doctor error:", err)
        raise


def insert_appointment(doctor_email, patient_email, date, time):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO appointments (doctor_email, patient_email, date, time)
            VALUES (%s, %s, %s, %s)
        """, (doctor_email, patient_email, date, time))
        conn.commit()
        conn.close()
    except Error as e:
        print("Insert appointment error:", e)
        raise e

# ------------------ Validation ------------------

def validate_user(email, password, role):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        table = "doctors" if role == "Doctor" else "patients"
        cursor.execute(f"""
            SELECT * FROM {table} WHERE email = %s AND password = %s
        """, (email, password))
        result = cursor.fetchone()
        conn.close()
        return result
    except Error as e:
        print("Validation error:", e)
        return None