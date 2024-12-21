import streamlit as st
import os
import google.generativeai as genai
from PyPDF2 import PdfReader
import time

# Set page configuration
st.set_page_config(
    page_title="PDF Summarizer",
    page_icon="📄",
    layout="wide"
)

# Configure Gemini API
def setup_gemini():
    # Get API key from Streamlit secrets or environment variable
    api_key = st.text_input("Enter your Gemini API Key:", type="password")
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to create summary prompt
def create_summary_prompt(text):
    return f"""Please provide a comprehensive summary of the following text, 
    highlighting key points and main ideas:\n\n{text}"""

# Function to get response from Gemini
def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Main function
def main():
    st.title("PDF Document Summarizer")
    
    # Setup sidebar
    st.sidebar.title("About")
    st.sidebar.info("This app helps you summarize PDF documents using Google's Gemini AI.")
    
    # Setup Gemini
    if not setup_gemini():
        st.warning("Please enter your Gemini API key to continue.")
        return
    
    # File upload
    uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])
    
    if uploaded_file is not None:
        with st.spinner("Reading PDF..."):
            # Extract text from PDF
            text = extract_text_from_pdf(uploaded_file)
            st.text_area("Extracted Text", text, height=200)
            
        if st.button("Generate Summary"):
            with st.spinner("Generating summary..."):
                # Create prompt and get response
                prompt = create_summary_prompt(text)
                summary = get_gemini_response(prompt)
                
                # Display summary
                st.subheader("Summary")
                st.write(summary)
                
                # Add download button for summary
                st.download_button(
                    label="Download Summary",
                    data=summary,
                    file_name="summary.txt",
                    mime="text/plain"
                )

if __name__ == "__main__":
    main()