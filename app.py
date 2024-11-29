import streamlit as st
import pandas as pd
from io import BytesIO
from materialsearch import SemanticSearch
import json


# Defintions
def beautify_json(match):
    return f"{match['material_number']}: {match['description']} (Score: {match['percent']}%)"

def get_matches(query,max_search):
    queries = [query]
    search= search_engine.search(queries, top_k=max_search)
    results = json.loads(search)[0]
    query = results['query']
    return results['matches']

def update_max_search(value):
    st.session_state.max_search = value

# add caching of model
@st.cache_resource
def load_search_engine():
    # Initialize the search engine and return it
    # supported models: 'sentence_transformer' and 'bert'. Noted that bert performs poorly, code commented out, need a spike.
    return SemanticSearch(data_file='materials.json',model_type='sentence_transformer')

# Main App
st.set_page_config(page_title="Material Matcher", page_icon=":guardsman:")
tab1, tab2, tab3 = st.tabs(["Search", "Wizard", "Settings"])
search_engine = load_search_engine()
# Set the value if it hasn't been initialized before
if "max_search" not in st.session_state:
    update_max_search(5)

with tab1:
    st.subheader('Cognitive Search')    
    st.write("Find matching inventory items with text search:")
    search_query = st.text_input("Enter description", placeholder="Enter description", label_visibility="collapsed")

    # Filter results based on search query
    if search_query:
        matches = get_matches(search_query,st.session_state.max_search)
        st.write("Results based on rank order:")
        for match in matches:
            st.text(beautify_json(match))
    st.write("\n")

        
# Batch processing via file upload
with tab2:
    st.subheader('Excel Wizard')
    st.text("Upload an Excel file to bulk search for inventory items, following the steps below:")
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
            df['material_id'] = None

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
                    df.at[index, 'material_id'] = selection['material_number']
                

            
            # Display editable dataframe
            st.write("\n")
            st.markdown("##### Step 3: Review output")
            st.write("\n")
            edited_df = st.data_editor(df, num_rows="dynamic")
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
    st.write("\n")
    new_max_search  = st.slider("Maximum search results", min_value=1, max_value=20, value=5)
    update_max_search(new_max_search)