# entity_extractor.py

import pdfplumber
from pptx import Presentation
import pytesseract
from PIL import Image
import json
import os
import re

try:
    from langchain_ollama import OllamaLLM
except ImportError:
    print("Please install langchain-ollama: pip install langchain-ollama")
    OllamaLLM = None

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text

def extract_text_from_pptx(pptx_path):
    text = ""
    prs = Presentation(pptx_path)
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text += shape.text + "\n"
    return text

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)

def extract_entities_with_llama(text):
    if OllamaLLM is None:
        print("OllamaLLM is not available.")
        return []

    prompt = (
        "Extract at least 20 entities from the following text. "
        "Return a JSON array with key and type fields for each entity. "
        "Format output as valid JSON only:\n\n"
        + text
    )

    try:
        llm = OllamaLLM(model="llama3.2")
        response = llm.invoke(prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Try to extract any valid JSON array from the response
            match = re.search(r"\[[\s\S]*?\]", response)
            if match:
                try:
                    return json.loads(match.group(0))
                except json.JSONDecodeError:
                    return []
        return []
    except Exception as e:
        print("Error using Ollama LLM:", e)
        return []

def process_files(file_paths):
    combined_text = ""
    for file_path in file_paths:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            combined_text += extract_text_from_pdf(file_path) + "\n"
        elif ext in [".ppt", ".pptx"]:
            combined_text += extract_text_from_pptx(file_path) + "\n"
        elif ext in [".png", ".jpg", ".jpeg"]:
            combined_text += extract_text_from_image(file_path) + "\n"
        else:
            print(f"Unsupported file type: {file_path}")

    return extract_entities_with_llama(combined_text)
