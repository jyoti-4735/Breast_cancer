import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import streamlit as st
import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import numpy as np
import cv2
from io import BytesIO
from reportlab.pdfgen import canvas
from datetime import date
from model import ImprovedCNN
from utils.database import connect_to_db
import pandas as pd


# --------- Grad-CAM ----------
def generate_gradcam_overlay(model, input_tensor, target_layer):
    gradients = []
    activations = []

    def save_activations(module, input, output):
        activations.append(output)

    def save_gradients(module, grad_input, grad_output):
        gradients.append(grad_output[0])

    handle1 = target_layer.register_forward_hook(save_activations)
    handle2 = target_layer.register_full_backward_hook(save_gradients)

    model.eval()
    input_tensor.requires_grad = True
    output = model(input_tensor)
    pred_class = torch.argmax(output, dim=1).item()
    score = output[0, pred_class]
    model.zero_grad()
    score.backward()

    grads = gradients[0].cpu().detach().numpy()[0]
    acts = activations[0].cpu().detach().numpy()[0]
    weights = np.mean(grads, axis=(1, 2))

    cam = np.zeros(acts.shape[1:], dtype=np.float32)
    for i, w in enumerate(weights):
        cam += w * acts[i]

    cam = np.maximum(cam, 0)
    cam = cv2.resize(cam, (224, 224))
    cam = (cam - cam.min()) / (cam.max() + 1e-8)

    img_np = input_tensor.squeeze().permute(1, 2, 0).cpu().detach().numpy()
    img_np = (img_np * 255).astype(np.uint8)

    heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(img_np, 0.6, heatmap, 0.4, 0)

    handle1.remove()
    handle2.remove()
    return overlay


# --------- PDF ----------
def generate_pdf_report(prediction_text):
    buffer = BytesIO()
    c = canvas.Canvas(buffer)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 800, "Breast Cancer Detection Report")

    c.setFont("Helvetica", 12)
    c.drawString(100, 770, f"Prediction Result: {prediction_text}")
    c.drawString(100, 750, f"Generated on: {date.today().strftime('%B %d, %Y')}")
    c.drawString(100, 730, "Thank you for using our AI Diagnostic Tool.")

    c.save()
    buffer.seek(0)
    return buffer


# --------- Appointment Request ----------
def request_appointment_ui(patient_email):
    st.markdown("### 📅 Request an Appointment")

    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute("SELECT email, name FROM doctors")
        doctors = cursor.fetchall()

        if not doctors:
            st.warning("No doctors available.")
            return

        doc_choices = {f"{doc[1]}": doc[0] for doc in doctors}
        selected_doc = st.selectbox("Choose a Doctor", list(doc_choices.keys()))
        selected_doc_email = doc_choices[selected_doc]

        appt_date = st.date_input("Preferred Date", min_value=date.today())
        appt_time = st.time_input("Preferred Time")

        if st.button("Request Appointment"):
            cursor.execute("""
                INSERT INTO appointments (doctor_email, patient_email, date, time, status)
                VALUES (?, ?, ?, ?, ?)
            """, (selected_doc_email, patient_email, str(appt_date), str(appt_time), "pending"))

            conn.commit()
            st.success("✅ Appointment request submitted successfully.")

        conn.close()

    except Exception as e:
        st.error(f"Error: {e}")


# --------- MAIN DASHBOARD ----------
def patient_dashboard():
    st.markdown("""
    <div style="background-color: rgba(13, 59, 102, 0.85); padding: 1rem 2rem; border-radius: 10px; margin-bottom: 20px;">
        <h1 style="color: white;">🧍‍♀ Patient Dashboard</h1>
        <p style="color: white;">Upload your histopathology image for AI-based Breast Cancer detection.</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("📤 Upload an Image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", width=300)

        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor()
        ])

        input_tensor = transform(image).unsqueeze(0)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        with st.spinner("🔎 Running AI analysis..."):
            model = ImprovedCNN()
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            model_path = os.path.join(BASE_DIR, "model.pth")
            model.load_state_dict(torch.load(model_path, map_location=device))
            model.to(device)
            model.eval()

            input_tensor = input_tensor.to(device)
            output = model(input_tensor)

            pred_class = torch.argmax(output, dim=1).item()
            confidence = F.softmax(output, dim=1)[0][pred_class].item() * 100

            classes = ["Benign", "Malignant"]
            result_text = f"{classes[pred_class]} ({confidence:.2f}%)"

        if pred_class == 0:
            st.success(f"✅ Prediction: {result_text}")
        else:
            st.error(f"⚠ Prediction: {result_text}")
            request_appointment_ui(st.session_state.username)

        pdf_buffer = generate_pdf_report(result_text)
        st.download_button("📄 Download Report", data=pdf_buffer, file_name="report.pdf")

    # -------- Appointment History --------
    st.subheader("🗂 Your Appointment History")

    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT d.name, a.date, a.time, a.status
            FROM appointments a
            JOIN doctors d ON a.doctor_email = d.email
            WHERE a.patient_email = ?
            ORDER BY a.date DESC, a.time DESC
        """, (st.session_state.username,))

        history = cursor.fetchall()

        if history:
            df = pd.DataFrame(history, columns=["Doctor", "Date", "Time", "Status"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No appointments yet.")

        conn.close()

    except Exception as e:
        st.error(f"Error: {e}")