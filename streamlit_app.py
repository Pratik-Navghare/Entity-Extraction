import streamlit as st
import tempfile
import os
import json
from entity_extractor import process_files

st.title("Entity Extraction from Documents")

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
        with st.spinner("Extracting entities..."):
            temp_dir = tempfile.mkdtemp()
            file_paths = []
            for uploaded_file in uploaded_files:
                file_path = os.path.join(temp_dir, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                file_paths.append(file_path)

            entities = process_files(file_paths)
            if entities:
                output_placeholder.json(entities)
            else:
                output_placeholder.text("No entities extracted or an error occurred.")

with st.sidebar:
    st.title("Team 2")
    st.markdown(
        """
        <div style="color:#222; font-weight:bold;">
        <p><strong>Credits:</strong></p>
        <ul>
            <li>Pratik Navghare</li>
            <li>Yash Mankar</li>
            <li>Aniket Nikhumb</li>
            <li>Tushar Dale</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
