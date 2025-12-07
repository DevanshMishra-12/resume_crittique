import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Resume Critiquer", page_icon="📃", layout="centered")

st.title("AI Resume Critiquer")
st.markdown("Upload your resume and get AI-powered feedback tailored to your needs!")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY is not set. Please add it to your environment or .env file.")
    st.stop()

uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])
job_role = st.text_input("Enter the job role you're targeting (optional)")

analyze = st.button("Analyze Resume")

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extracts text from a PDF file given its bytes."""
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
    text = ""
    for page in pdf_reader.pages:
        # page.extract_text() can return None
        page_text = page.extract_text() or ""
        text += page_text + "\n"
    return text

def extract_text_from_file(uploaded) -> str:
    """Handles both PDF and TXT file types."""
    file_bytes = uploaded.read()
    if not file_bytes:
        return ""
    if uploaded.type == "application/pdf":
        return extract_text_from_pdf(file_bytes)
    # assume text file
    try:
        return file_bytes.decode("utf-8", errors="ignore")
    except Exception:
        return ""

if analyze and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file)

        if not file_content or not file_content.strip():
            st.error("The uploaded file does not contain any readable content.")
            st.stop()

        target_text = job_role if job_role.strip() else "general job applications"

        prompt = f"""
You are an expert resume reviewer with years of experience in HR and recruitment.

Please analyze the following resume and provide **clear, constructive feedback**.

Focus on:
1. Content clarity and impact
2. Skills presentation
3. Experience descriptions
4. Specific improvements for **{target_text}**

Resume:
\"\"\" 
{file_content}
\"\"\"

Now provide:
- A brief summary of the overall impression
- Strengths (bullet points)
- Weaknesses / areas to improve (bullet points)
- Specific rewrite suggestions for key sections (e.g., summary, experience bullets)
- Any tailoring tips for {target_text}.
"""

        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # or "gpt-4.1-mini" if available to you
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert resume reviewer with years of experience in HR and recruitment."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        st.markdown("### Analysis Results")
        st.markdown(response.choices[0].message.content)

    except Exception as e:
        st.error(f"An error occurred while analyzing the resume:\n\n`{str(e)}`")
