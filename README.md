# Material Matcher
A Streamlit app with semantic search

## Installation steps

1. Setup python virtual environment
```
python3 -m venv venv
source venv/bin/activate
```

2. Install pytorch for for M1 Mac
```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

3. Install other packages
```
pip install sentence-transformers streamlit openpyxl
```

4. (optional) Install Jupyter notebook for testing different models
```
pip install notebook
```

## Run locally

Run steamlit:
```
streamlit run app.py
```
## About the App
1. There are 3 main streamlit pages:
- app.py: The primary application
- login.py: Login page
- main.py: Main landing page

2. The `models` folder contains the source data for creating embeddings and the semantic search code

3. The `tools` folder are not essential to the app. It contains,
- `test_data.xlsx`: a test file to test upload of material and services description by batch
- `error_file.xlsx`: this is not an excel file, but rename with `.xlsx' extension
- `empty_file.xlxs`: to test exception handling of loading empty excel file.
- `excel_to_json.py`: for converting excel into json that is used for generating the embeddings