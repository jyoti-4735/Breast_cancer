import streamlit as st
import re  # for email validation


def show():
    # Header section with styling
    

    # --- Contact Form ---
    with st.form(key="contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Message", height=150)
        submit_button = st.form_submit_button(label="Send ✉")

    # --- Validation & Response ---
    if submit_button:
        if not name or not email or not message:
            st.error("Please fill out all fields before sending!")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.error("Please enter a valid email address.")
        else:
            # Placeholder for email backend integration
            st.success(f"Thank you {name}! Your message has been received. We'll get back to you soon. 😊")
            # Here you can integrate SMTP or a third-party email service
