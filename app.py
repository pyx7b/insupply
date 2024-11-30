import streamlit as st
from login import login_page
from main import main_page

# If not initialise, initialise to isLogin to False
if 'isLogin' not in st.session_state:
    st.session_state['isLogin'] = False

#Check if user has logged in
if st.session_state['isLogin']:
    main_page()
else:
    # Redirect to login page if not authenticated
    login_page()

