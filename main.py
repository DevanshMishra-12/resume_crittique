import streamlit as st

st.set_page_config(page_title="Resume Critique App", page_icon="📄", layout="centered")

st.title("📄 Resume Critique App")
st.write("Upload your resume and get quick feedback on structure, clarity, and impact.")

option = st.radio("How do you want to submit your resume?", ["Paste text", "Upload .docx (not implemented)"])

resume_text = ""

if option == "Paste text":
    resume_text = st.text_area(
        "Paste your resume content here:",
        height=300,
        placeholder="Paste your resume text (education, experience, projects, skills, etc.)"
    )
elif option == "Upload .docx (not implemented)":
    uploaded_file = st.file_uploader("Upload your resume (.docx)", type=["docx"])
    st.info("Docx parsing not implemented yet. For now, please use 'Paste text' option.")
    if uploaded_file:
        st.warning("Feature under development. Switch to 'Paste text' for now.")

if st.button("Get Critique"):
    if not resume_text.strip():
        st.error("Please paste your resume text first.")
    else:
        st.subheader("✅ High-level Feedback")
        st.write(
            "- Overall clarity: Your resume should be concise and easy to scan.\n"
            "- Use bullet points for achievements, not paragraphs.\n"
            "- Start bullet points with strong action verbs (e.g., *Developed*, *Led*, *Improved*).\n"
        )

        st.subheader("📌 Suggestions for Improvement")
        st.write(
            "- Make sure each experience has clear **Role**, **Company**, **Location**, and **Dates**.\n"
            "- Quantify impact whenever possible (e.g., *Increased traffic by 30%*, *Reduced processing time by 40%*).\n"
            "- Group projects and skills clearly into separate sections.\n"
        )

        st.subheader("🧠 Keywords & ATS Tips")
        st.write(
            "- Include relevant keywords from the job description.\n"
            "- Avoid too many graphics or complex layouts that confuse ATS parsers.\n"
            "- Use simple headings like **Experience**, **Education**, **Projects**, **Skills**.\n"
        )

        st.success("This is a basic template critique. You can later integrate an AI model/API for smarter feedback.")
