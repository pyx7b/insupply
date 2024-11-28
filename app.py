import streamlit as st
import pandas as pd
from io import BytesIO
from materialsearch import SemanticSearch
import json


# Defintions
def beautify_json(match):
    return f"{match['material_number']}: {match['description']} (Score: {match['percent']}%)"

def get_matches(query):
    queries = [query]
    search= search_engine.search(queries)
    results = json.loads(search)[0]
    query = results['query']
    return results['matches']

# add caching of model
@st.cache_resource
def load_search_engine():
    # Initialize the search engine and return it
    # supported models: 'sentence_transformer' and 'bert'. Noted that bert performs poorly, code commented out, need a spike.
    return SemanticSearch(data_file='materials.json',model_type='sentence_transformer')

# Main App
st.set_page_config(page_title="Material Matcher", page_icon=":guardsman:")

# Custom CSS to remove the label and its space
st.markdown(
    """
    <style>
    .stSelectbox label {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

search_engine = load_search_engine()

st.subheader('Search')
search_query = st.text_input("Key in description to find matching inventory items:", placeholder="")

# Filter results based on search query
if search_query:
    matches = get_matches(search_query)
    st.text("Results:")
    for match in matches:
        st.text(beautify_json(match))
    st.markdown("*Results are ranked based on closest match with highest score listed on top.*")
st.write("\n")
st.divider()

# Batch processing via file upload
st.subheader('Batch Processing')
st.write("&nbsp;")
st.markdown("##### Step 1: Upload an Excel file")
st.markdown("The excel file should contain a column header labelled as `description`")
uploaded_file = st.file_uploader("",type=["xlsx"])
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

        st.write("&nbsp;")
        st.markdown("##### Step 2: Select material or service number")
        # Loop through each row in dataframe
        for index, row in df.iterrows():
            matches = get_matches(row['description']) 
            #print output in columns
            col1, col2 = st.columns([1,3])
            with col1:
                st.text(row['description'])

            with col2:
                # Display the matches and let the user select one
                selection = st.selectbox("",
                    matches,
                    index=None,
                    placeholder="Select best match",
                    format_func=beautify_json  # Beautify the display
                )
            if selection:
                df.at[index, 'material_id'] = selection['material_number']
            

        
        # Display editable dataframe
        st.write("&nbsp;")
        st.markdown("##### Step 3: Review output")
        st.write("&nbsp;")
        edited_df = st.data_editor(df, num_rows="dynamic")
        # Write to excel object
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            edited_df.to_excel(writer, index=False, sheet_name="Sheet1")
        output.seek(0)  # Reset the pointer to the beginning of the file

        # Download excel file
        st.download_button(
            label="Download Excel",
            data=output,
            file_name="updated_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    except Exception as e:
        # Handle errors
        st.error(f"Error: {e}", icon="❌")      