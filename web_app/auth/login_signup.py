import streamlit as st
import re
from utils.session import login_user
from utils.database import insert_doctor, insert_patient, validate_user

# ---------------- Validation Utilities ----------------
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

def is_valid_phone(phone):
    pattern = r"^\d{10}$"
    return re.match(pattern, phone)

# ---------------- Login / Register ----------------
def login_signup():
    with st.container():
        st.title("🔐 Login / Signup")
        tab1, tab2 = st.tabs(["Login", "Register"])

        # ----------- LOGIN TAB -----------
        with tab1:
            st.subheader("Login")
            login_role = st.selectbox("Login as", ["Patient", "Doctor"], key="login_role")
            login_email = st.text_input("Email", key="login_email")
            login_password = st.text_input("Password", type="password", key="login_password")

            if st.button("Login", key="login_button"):
                if login_email and login_password:
                    user = validate_user(login_email, login_password, login_role)
                    if user:
                        st.success(f"Welcome back, {login_role} {user[1]}")
                        login_user(username=user[2], role=login_role)
                        st.experimental_rerun()
                    else:
                        st.error("Invalid credentials. Please try again.")
                else:
                    st.warning("Please enter both email and password")

        # ----------- REGISTER TAB -----------
        with tab2:
            st.subheader("Register")
            register_role = st.selectbox("Register as", ["Patient", "Doctor"], key="register_role")

            if register_role == "Doctor":
                doc_name = st.text_input("Full Name", key="doc_name")
                doc_email = st.text_input("Email", key="doc_email")
                doc_qualification = st.text_input("Qualification", key="doc_qualification")
                doc_experience = st.number_input("Years of Experience", min_value=0, key="doc_experience")
                doc_specialization = st.text_input("Specialization", key="doc_specialization")
                doc_password = st.text_input("Password", type="password", key="doc_password")
                doc_confirm = st.text_input("Confirm Password", type="password", key="doc_confirm")

                if st.button("Register Doctor", key="register_doctor"):
                    if not all([doc_name, doc_email, doc_qualification, doc_specialization, doc_password, doc_confirm]):
                        st.warning("Please fill out all the fields.")
                    elif not is_valid_email(doc_email):
                        st.error("Please enter a valid email address.")
                    elif doc_password != doc_confirm:
                        st.error("Passwords do not match.")
                    else:
                        try:
                            insert_doctor(doc_name, doc_email, doc_qualification, doc_specialization, doc_experience, doc_password)
                            st.success("✅ Doctor registered successfully. Please login.")
                        except Exception as e:
                            st.error("❌ Email already registered or DB error.")

            elif register_role == "Patient":
                pat_name = st.text_input("Full Name", key="pat_name")
                pat_email = st.text_input("Email", key="pat_email")
                pat_phone = st.text_input("Phone Number", key="pat_phone")
                pat_password = st.text_input("Password", type="password", key="pat_password")
                pat_confirm = st.text_input("Confirm Password", type="password", key="pat_confirm")

                if st.button("Register Patient", key="register_patient"):
                    if not all([pat_name, pat_email, pat_phone, pat_password, pat_confirm]):
                        st.warning("Please fill out all the fields.")
                    elif not is_valid_email(pat_email):
                        st.error("Please enter a valid email address.")
                    elif not is_valid_phone(pat_phone):
                        st.error("Phone number must be 10 digits.")
                    elif pat_password != pat_confirm:
                        st.error("Passwords do not match.")
                    else:
                        try:
                            insert_patient(pat_name, pat_email, pat_phone, pat_password)
                            st.success("✅ Patient registered successfully. Please login.")
                        except Exception as e:
                            st.error("❌ Failed to register.")
                            st.exception(e)