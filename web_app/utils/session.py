import streamlit as st

def init_session():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "role" not in st.session_state:
        st.session_state.role = None
    if "username" not in st.session_state:
        st.session_state.username = None

def login_user(username, role):
    st.session_state.authenticated = True
    st.session_state.username = username
    st.session_state.role = role

def logout_user():
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.role = None

def is_authenticated():
    return st.session_state.authenticated

def get_user_info():
    return st.session_state.username, st.session_state.role
