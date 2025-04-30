# streamlit_app.py

import streamlit as st
import tempfile
import os
import requests
import time
from entity_extractor import process_files

# Replace with your real Lambda API Gateway URL
QUOTE_API_URL = "https://your-api-id.execute-api.region.amazonaws.com/default/getQuote"

def fetch_random_quote():
    try:
        response = requests.get(QUOTE_API_URL)
        if response.status_code == 200:
            data = response.json()
            return f"\"{data['text']}\" — {data.get('author', 'Unknown')}"
    except:
        return "Fetching quote..."

st.set_page_config(page_title="Entity Extractor", layout="centered")
st.title("📄 Entity Extraction from Documents")

uploaded_files = st.file_uploader(
    "Upload PDF, PNG, JPEG, PPT, PPTX files",
    type=["pdf", "png", "jpeg", "jpg", "ppt", "pptx"],
    accept_multiple_files=True
)

output_placeholder = st.empty()

if st.button("Generate Entities"):
    if not uploaded_files:
        st.warning("Please upload at least one file.")
    else:
        with st.spinner("Preparing files..."):
            temp_dir = tempfile.mkdtemp()
            file_paths = []
            for uploaded_file in uploaded_files:
                file_path = os.path.join(temp_dir, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                file_paths.append(file_path)

        quote_placeholder = st.empty()
        start_time = time.time()
        processing = True
        entities = []

        while processing:
            elapsed = time.time() - start_time
            if elapsed < 10:  # simulate progress
                quote_placeholder.info(fetch_random_quote())
                time.sleep(3)
            else:
                with st.spinner("Extracting entities..."):
                    entities = process_files(file_paths)
                processing = False

        quote_placeholder.empty()

        if entities:
            output_placeholder.json(entities)
        else:
            output_placeholder.warning("No entities extracted or an error occurred.")

with st.sidebar:
    st.header("👥 Team 2")
    st.markdown(
        """
        - Pratik Navghare  
        - Yash Mankar  
        - Aniket Nikhumb  
        - Tushar Dale  
        """
    )
