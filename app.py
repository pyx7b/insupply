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
    return SemanticSearch(data_file='materials.json')

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
    st.markdown("*Result is ranked based on closest match with highest score listed on top.*")
st.write("\n")
st.divider()
st.subheader('Batch Processing')
st.write("&nbsp;")
st.markdown("##### Step 1: Upload an Excel file")
uploaded_file = st.file_uploader("",type=["xlsx"])

if uploaded_file:
    # Load the Excel file into a Pandas DataFrame
    df = pd.read_excel(uploaded_file)
    # Add Material ID Column
    df['Material ID'] = None

    st.write("&nbsp;")
    st.markdown("##### Step 2: Select material or service number")
    # Loop through each row in dataframe
    for index, row in df.iterrows():
        matches = get_matches(row['Description']) 
        #print output in columns
        col1, col2 = st.columns([1,3])
        with col1:
            st.text(row['Description'])

        with col2:
            # Display the matches and let the user select one
            selection = st.selectbox("",
                matches,
                index=None,
                placeholder="Select best match",
                format_func=beautify_json  # Beautify the display
            )
        if selection:
            df.at[index, 'Material ID'] = selection['material_number']
        

    # Display editable dataframe
    st.write("&nbsp;")
    st.markdown("##### Step 3: Review output")
    st.write("&nbsp;")
    edited_df = st.data_editor(df, num_rows="dynamic")


    # Single download button
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        edited_df.to_excel(writer, index=False, sheet_name="Sheet1")
    output.seek(0)  # Reset the pointer to the beginning of the file

    # Provide a download button
    st.download_button(
        label="Download Excel",
        data=output,
        file_name="updated_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


