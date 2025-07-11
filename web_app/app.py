import streamlit as st
from pages import home, about, contact
from auth.login_signup import login_signup
from dashboard.patient_dashboard import patient_dashboard
from dashboard.doctor_dashboard import doctor_dashboard
from utils.session import init_session, logout_user, is_authenticated
from utils.database import init_db

# --- Page Config ---
st.set_page_config(
    page_title="Breast Cancer Detection",
    layout="wide",
    page_icon="🏥",
    initial_sidebar_state="collapsed",
)

# --- Hide Default Streamlit UI ---
hide_streamlit_style = """
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- Initialize Session and Database ---
init_session()
init_db()

# --- Create Custom Navbar ---
def navbar():
    active_page = st.session_state.get("page", "Home")

    def nav_link(name, label=None):
        label = label or name
        style = "color: #0d47a1; margin-left: 20px; font-weight: bold; text-decoration: none; font-size: 18px;"
        if name == active_page:
            style = "color: #d6336c; margin-left: 20px; font-weight: bold; text-decoration: underline; font-size: 18px;"
        return f'<a style="{style}" href="?page={name}">{label}</a>'

    st.markdown(
        f"""
        <style>
            .navbar {{
                background-color: #ffffff;
                padding: 10px 20px;
                border-radius: 16px;
                position: sticky;
                top: 0;
                z-index: 999;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }}
            .navbar-links a:hover {{
                color: #d6336c;
                text-decoration: underline;
            }}
            .navbar-logo {{
                display: flex;
                align-items: center;
            }}
            .navbar-logo img {{
                height: 50px;
                margin-right: 15px;
            }}
        </style>
        <div class="navbar">
            <div class="navbar-logo">
                <img src="https://cdn-icons-png.flaticon.com/512/2966/2966485.png" alt="Logo">
                <h3 style="color: #d6336c; margin: 0;">Breast Cancer Detection</h3>
            </div>
            <div class="navbar-links">
                {nav_link('Home')}
                {nav_link('About')}
                {nav_link('Contact')}
                {nav_link('LoginSignup', 'Login/Signup')}
            </div>
        </div>
        <br>
        """,
        unsafe_allow_html=True
    )

# --- Default page ---
if "page" not in st.session_state:
    st.session_state.page = "Home"

# --- Detect page change from URL ---
query_params = st.query_params
if "page" in query_params and query_params["page"]:
    st.session_state.page = query_params["page"]


# --- Show Navbar ---
navbar()

# --- Show Selected Page ---
if st.session_state.page == "Home":
    home.show()

elif st.session_state.page == "About":
    about.show()

elif st.session_state.page == "Contact":
    contact.show()

elif st.session_state.page == "LoginSignup":
    if not is_authenticated():
        login_signup()
    else:
        role = st.session_state.role
        if role == "Doctor":
            doctor_dashboard()
        elif role == "Patient":
            patient_dashboard()

# --- Logout Button after Login ---
if is_authenticated():
    if st.button("🚪 Logout"):
        logout_user()
        st.experimental_rerun()