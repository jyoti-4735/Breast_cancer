import streamlit as st

def show():
    st.markdown("""
    <div style="background-color: rgba(255,255,255,0.85); padding: 2rem; border-radius: 15px;">
        <h2 style="color: #0d47a1;">ℹ About Us</h2>
        <p style="font-size: 1.1rem; color: #333;">
            We are a passionate team combining expertise in healthcare, artificial intelligence, and digital health solutions.<br><br>
            Our goal is to revolutionize early breast cancer detection and improve patient outcomes globally.<br><br>
            <b>Vision:</b> Make reliable and accessible cancer screening a reality for everyone.<br><br>
            <b>Mission:</b> Integrate AI-driven diagnosis with compassionate care.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Meet the Minds Section ---
    st.markdown("""
    <div style="background-color: rgba(224, 247, 250, 0.85); padding: 2rem; border-radius: 15px;">
        <h2 style="color: #0d47a1; text-align: center;">👩‍💻 Meet the Minds</h2>
        <p style="font-size: 1.1rem; color: #333; text-align: center;">
            Our talented team is committed to delivering AI-driven healthcare solutions that make a real difference.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Team Cards ---
    team = [
        {
            "name": "Ms. Jyoti Kambar",
            "role": "AI Specialist",
            "image": "jyoti.jpg",  # Replace with real image URLs
            "linkedin": "https://linkedin.com/in/jyotikambar"
        },
        {
            "name": "Ms. Laxmi Patil",
            "role": "ML Engineer",
            "image": "https://via.placeholder.com/150",
            "linkedin": "https://linkedin.com/in/laxmipatil"
        },
        {
            "name": "Ms. Anusha Nagathan",
            "role": "Healthcare Consultant",
            "image": "https://via.placeholder.com/150",
            "linkedin": "https://linkedin.com/in/anushanagathan"
        },
        {
            "name": "Mr. Kishan Paramanji",
            "role": "Backend Developer",
            "image": "https://via.placeholder.com/150",
            "linkedin": "https://linkedin.com/in/kishanparamanji"
        },
    ]

    cols = st.columns(4)  # 4 team members side by side

    for idx, member in enumerate(team):
        with cols[idx]:
            st.markdown(f"""
            <div style="background-color: #ffffff; padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <img src="{member['image']}" style="width:110px; height:110px; object-fit:cover; border-radius:50%; margin-bottom: 1rem;">
                <h4 style="color: #0d3b66;">{member['name']}</h4>
                <p style="font-size: 1rem; color: #555;">{member['role']}</p>
                <a href="{member['linkedin']}" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="24" style="margin-top:10px;">
                </a>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- References Section ---
    st.markdown("""
    <div style="background-color: rgba(255,255,255,0.85); padding: 2rem; border-radius: 15px;">
        <h3 style="color: #0d47a1;">📚 References</h3>
        <ul style="font-size: 1.1rem; color: #333;">
            <li>Smith et al., "Deep Learning for Breast Cancer", Journal of Medical Imaging, 2023.</li>
            <li>Patel et al., "AI in Oncology: A Review", AI Healthcare, 2024.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)