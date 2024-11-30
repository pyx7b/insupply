import streamlit as st

def login_page():
    # Collect login information
    username = st.text_input("Username", value='python')
    password = st.text_input("Password", value='123456', type="password")

    # Check if login credentials are correct
    if st.button("Login"):
        if username == "python" and password == "123456":
            # Store username in session
            if 'user' not in st.session_state:
                st.session_state['user'] = username
            st.session_state['isLogin'] = True
            st.success("Login successful!")
            st.rerun()  # Rerun to refresh the app after login
        else:
            st.error("Invalid credentials. Please try again.")
