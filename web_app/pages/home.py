import streamlit as st

def show():
    # --- Main Section ---
    st.markdown("""
        <div style="background-color: rgba(255, 255, 255, 0.85); padding: 2rem; border-radius: 15px;">
            <h1 style="color: #d6336c; text-align: center;">🏠 Breast Cancer Detection using AI</h1>
            <p style="font-size: 1.2rem; color: #333; text-align: center;">
                Breast cancer remains one of the leading causes of mortality among women globally.<br><br>
                <b>Early detection saves lives</b> — and technology can be our strongest ally.<br><br>
                This application empowers doctors and patients to:
            </p>
            <ul style="font-size: 1.1rem; color: #333; padding-left: 3rem;">
                <li>🔬 Use AI to analyze histopathology images</li>
                <li>🧠 Predict cancerous conditions with high accuracy</li>
                <li>🗓 Manage appointments and consultations easily</li>
                <li>📅 View treatment schedules and reports</li>
            </ul><br>
            <p style="font-size: 1.2rem; color: #0d47a1; text-align: center;">
                🔍 Let's use technology to fight breast cancer together!
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""<br><hr><br>""", unsafe_allow_html=True)

    # --- Latest Research Papers Section ---
    st.markdown("""
        <div style="background-color: rgba(240, 248, 255, 0.85); padding: 2rem; border-radius: 15px;">
            <h2 style="color: #d6336c;">🔹 Latest Research Papers</h2>
            <ul style="font-size: 1.1rem; color: #333;">
                <li><b>Deep Learning for Breast Cancer Histopathological Image Classification:</b> A Survey (IEEE, 2023)</li>
                <li><b>Explainable AI for Breast Cancer Diagnosis:</b> Using Grad-CAM visualization (Nature, 2024)</li>
                <li><b>Impact of Early Detection Technologies:</b> Comparative Study in Developing Countries (Lancet Oncology, 2022)</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""<br><hr><br>""", unsafe_allow_html=True)

    # --- Breast Cancer News Section ---
    st.markdown("""
        <div style="background-color: rgba(255, 239, 239, 0.85); padding: 2rem; border-radius: 15px;">
            <h2 style="color: #d6336c;">📈 Breast Cancer Awareness News</h2>
            <ul style="font-size: 1.1rem; color: #333;">
                <li>WHO launches new global initiative to reduce breast cancer mortality by 2.5% every year (2024)</li>
                <li>AI models now outperform radiologists in early-stage cancer detection (Harvard Medical School, 2025)</li>
                <li>New blood test shows 99% accuracy in early breast cancer detection (Stanford, 2025)</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)