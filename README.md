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

