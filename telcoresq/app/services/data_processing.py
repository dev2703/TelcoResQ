import pandas as pd
import json
import re

def parse_file(uploaded_file):
    """
    Parses an uploaded file (CSV or JSON) into a pandas DataFrame.
    """
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.json'):
        data = json.load(uploaded_file)
        df = pd.json_normalize(data)
    else:
        raise ValueError("Unsupported file type. Please upload a CSV or JSON file.")
    return df 

def clean_text(text):
    """
    Cleans a single text string by converting to lowercase, removing punctuation,
    and stripping extra whitespace.
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = text.strip()
    return text

def preprocess_dataframe(df, text_columns):
    """
    Applies text cleaning to specified columns of a DataFrame.
    """
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)
    return df 