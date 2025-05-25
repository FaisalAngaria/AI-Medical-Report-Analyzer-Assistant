import streamlit as st
import google.generativeai as genai
import PyPDF2
from PIL import Image
import io
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Google PaLM API
genai.configure(api_key="AIzaSyCLLzlbcyXjglYBXb6sFbDyAfUr-gAz44k")

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def analyze_report(text):
    try:
        # Use Google PaLM to analyze the medical report
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content(
            f"You are a medical report analyzer. Please analyze this medical report and provide a simple explanation of the results:\n\n{text}"
        )
        return str(response.text)
    except Exception as e:
        return f"Error analyzing report: {str(e)}"

def main():
    st.title("Medical Report Analyzer")
    st.write("Upload your medical report (PDF) and get a simple explanation of the results")
    
    # File upload
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    
    if uploaded_file is not None:
        try:
            # Display the uploaded file
            st.write("File uploaded successfully!")
            
            # Extract text from PDF
            text = extract_text_from_pdf(uploaded_file)
            
            # Analyze the report
            if st.button("Analyze Report"):
                with st.spinner("Analyzing your report..."):
                    analysis = analyze_report(text)
                    st.subheader("Analysis Results")
                    st.write(analysis)
                    
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    main()
