import streamlit as st
from utils.database import connect_to_db
from utils.session import is_authenticated


def doctor_dashboard():
    st.title("👨‍⚕ Doctor Dashboard")
    st.markdown("""
    <h4 style='font-size:24px;'>Welcome Doctor! Review patient details and manage appointment requests below.</h4>
    """, unsafe_allow_html=True)

    if not is_authenticated():
        st.warning("You must be logged in to view this page.")
        return

    doctor_email = st.session_state.username
    st.success(f"🔐 Logged in as: {doctor_email}")

    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        # 🔹 Registered Patients
        st.subheader("📋 Registered Patients")
        cursor.execute("SELECT name, email, phone FROM patients")
        patients = cursor.fetchall()

        if patients:
            patient_data = []
            for idx, (name, email, phone) in enumerate(patients, 1):
                patient_data.append({
                    "#": idx,
                    "Name": name,
                    "Email": email,
                    "Phone": phone
                })
            st.table(patient_data)
        else:
            st.info("No patients registered.")

        # 🔹 Appointment Requests
        st.subheader("📅 Appointment Requests")

        cursor.execute("""
            SELECT a.id, p.name, a.date, a.time, a.status
            FROM appointments a
            JOIN patients p ON a.patient_email = p.email
            WHERE a.doctor_email = ?
            ORDER BY a.date DESC, a.time DESC
        """, (doctor_email,))

        appointments = cursor.fetchall()

        if appointments:
            for appt_id, patient_name, appt_date, appt_time, status in appointments:
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 2])

                    with col1:
                        st.markdown(f"""
                        <div style='font-size:18px;'><b>{patient_name}</b></div>
                        <div>📅 {appt_date} ⏰ {appt_time}</div>
                        """, unsafe_allow_html=True)

                    with col2:
                        status_color = {
                            "pending": "#FFA500",
                            "accepted": "#4CAF50",
                            "rejected": "#F44336"
                        }.get(status.lower(), "gray")

                        st.markdown(f"""
                        <span style='background-color:{status_color}; padding:6px 12px; border-radius:10px; color:white;'>
                        {status.capitalize()}
                        </span>
                        """, unsafe_allow_html=True)

                    with col3:
                        if status.lower() == "pending":
                            if st.button("✅ Accept", key=f"accept_{appt_id}"):
                                update_status(appt_id, "accepted")
                                st.rerun()

                            if st.button("❌ Reject", key=f"reject_{appt_id}"):
                                update_status(appt_id, "rejected")
                                st.rerun()

                st.markdown("<hr>", unsafe_allow_html=True)
        else:
            st.info("No appointment requests found.")

        conn.close()

    except Exception as e:
        st.error(f"Database error: {e}")


# 🔹 Update appointment status
def update_status(appointment_id, new_status):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE appointments SET status = ? WHERE id = ?",
            (new_status, appointment_id)
        )

        conn.commit()
        conn.close()

    except Exception as e:
        st.error(f"Failed to update appointment status: {e}")