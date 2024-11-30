import streamlit as st
import pandas as pd
from io import BytesIO
from models import search
import json
import uuid

#Define Logout function 
def logout():
    st.session_state.clear()  # Clear session state
    st.success("Logged out successfully!")
    st.rerun()  # Rerun the app to show the login page


# Define a reusable function for toggle buttons
def toggle_component(label1, label2):
    with st.container():
        # Create two columns for side-by-side toggles
        col1, col2 = st.columns([1,4])
        
        # Toggle in the first column
        with col1:
            toggle_1 = st.checkbox(label1, value=True)
        
        # Toggle in the second column
        with col2:
            toggle_2 = st.checkbox(label2, value=True)
        
        # Validation: Ensure at least one toggle is activated
        if not toggle_1 and not toggle_2:
            st.warning(f"At least one of {label1} or {label2} must be selected")

        # Return the states of the toggles
        return toggle_1, toggle_2

#Define a resuable title component with top right menu
def title_menu(label, key):
    with st.container():
        menu_col1, menu_col2 = st.columns([7, 1])
        with menu_col1:
            st.subheader(label)
        with menu_col2:
            if st.button("Logout",key=key):
                logout()

# Defintions
def beautify_json(match):
    return f"{match['material_number']}: {match['description']} (Score: {match['score']}%)"

def get_matches(query,max_search):
    queries = [query]
    search= search_engine.search(queries, top_k=max_search)
    results = json.loads(search)[0]
    query = results['query']
    return results['matches']

# add caching of model
@st.cache_resource
def load_search_engine():
    #load datafile
    datafile = 'models/materials.json'
    # Initialize the search engine and return it
    # supported models: 'sentence_transformer' and 'bert'. Noted that bert performs poorly, code commented out, need a spike.
    return search.SemanticSearch(data_file=datafile, model_type='sentence_transformer')

def update_max_search(value):
    st.session_state.max_search = value

# Load search engine into memory 
search_engine = load_search_engine()

# Main App
def main_page():
    title_menu("", "pri_logout_but")
    tab1, tab2, tab3, tab4 = st.tabs(["Search", "Wizard", "Settings", "Help"])
    # Set the value if it hasn't been initialized before
    if "max_search" not in st.session_state:
        update_max_search(5) #default to 5

    with tab1:        
        st.subheader('Cognitive Search')
        st.write("\n")
        st.write("\n")
        #material_state, service_state = toggle_component("Material", "Service")
        st.write("Find similiar inventory items by description:")
        search_query = st.text_input("Enter description", placeholder="Enter description", label_visibility="collapsed")
        st.write("\n")
        # Filter results based on search query
        if search_query:
            matches = get_matches(search_query,st.session_state.max_search)
            st.write(f"Top {st.session_state.max_search} results based on proximity score:")
            matches_df = pd.DataFrame(matches)
            matches_df.index.name = 'id'
            matches_df.index = matches_df.index + 1 # set index to start from 1
            matches_df['score'] = matches_df['score'].apply(lambda x: f'{x}%')
            st.dataframe(matches_df, use_container_width=True)
        st.write("\n")

            
    # Batch processing via file upload
    with tab2:
        st.subheader('Excel Wizard')
        st.text("Upload an Excel file to bulk search for inventory items following the steps below.")
        st.write("&nbsp;")
        st.markdown("##### Step 1: Upload file")
        st.markdown("Excel file should contain a column header labelled as `description`")
        uploaded_file = st.file_uploader("Upload excel",type=["xlsx"],label_visibility="collapsed")
        if uploaded_file:
            try:
                # Show spinner while loading the file
                with st.spinner('Loading Excel file...'):
                    # Load the Excel file into a Pandas DataFrame
                    df = pd.read_excel(uploaded_file)
                    if df.empty:
                        st.error("❌ Error: The uploaded file is empty.")
                        st.stop() # Halts further execution

                # normalised the columns to lower case and replace space with underscore
                df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
                # Check for missing columns
                required_columns = {"description"}  # Define the required columns
                missing_columns = required_columns - set(df.columns)
                if missing_columns:
                    st.error(f"❌ Error: The uploaded file is missing required columns: {', '.join(missing_columns)}")
                    st.stop()  # Halts further execution
                # Add Material ID Column
                df.insert(1, 'material_number', None)

                st.write("\n")
                st.markdown("##### Step 2: Select material or service number")
                st.write("\n")
                # Loop through each row in dataframe
                for index, row in df.iterrows():
                    matches = get_matches(row['description'],st.session_state.max_search) 
                    #print output in columns
                    col3, col4 = st.columns([1,3])
                    with col3:
                        st.text(row['description'])

                    with col4:
                        # Display the matches and let the user select one
                        selection = st.selectbox("Select best match",
                            matches,
                            index=None,
                            placeholder="Select best match",
                            format_func=beautify_json,
                            label_visibility="collapsed"
                        )
                    if selection:
                        df.at[index, 'material_number'] = selection['material_number']
                    
                # Display editable dataframe
                st.write("\n")
                st.markdown("##### Step 3: Review output")
                st.write("\n")
                edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
                # Write to excel object
                output = BytesIO()
                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    edited_df.to_excel(writer, index=False, sheet_name="Sheet1")
                output.seek(0)  # Reset the pointer to the beginning of the file
                st.write("\n")
                # Download excel file
                st.download_button(
                    label="Download Excel",
                    data=output,
                    file_name="updated_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    type="secondary"
                )

            except Exception as e:
                # Handle errors
                st.error(f"Error: {e}", icon="❌")     
        st.write("\n")

    with tab3:
        st.subheader('Your Preferences')
        new_max_search  = st.slider("Maximum search results", min_value=1, max_value=50, value=5)
        update_max_search(new_max_search)

    with tab4:
        st.subheader('Help')
        with st.container(border=True):
            st.markdown("##### Questions? Ideas? Random Thoughts? We’re Listening!")
            st.markdown("Got a question or an idea that’s absolutely genius? We bet you do! Send us an [email](mailto:insupply@htx.ht.gov.sg), and we’ll get back to you as soon as we finish our coffee &#9749;", unsafe_allow_html=True)
