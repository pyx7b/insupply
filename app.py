import streamlit as st
from login import login_page
from main import main_page

# High streamlit right deploy button and menu
st.markdown("""
<style>
    .stAppToolbar{
        display: none;
    }
</style>
            
<footer style="text-align:center;">
    <p>A project by Ng Pan Yong @pyx7b</p>
</footer>
""", unsafe_allow_html=True)

# If not initialise, initialise to isLogin to False
if 'isLogin' not in st.session_state:
    st.session_state['isLogin'] = False

#Check if user has logged in
if st.session_state['isLogin']:
    main_page()
else:
    # Redirect to login page if not authenticated
    login_page()

