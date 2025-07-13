
import streamlit as st
import os
from resume_parser import extract_text_from_pdf
from job_recommender import load_jobs, recommend_jobs

st.set_page_config(page_title="Skill Sync", layout="wide")


st.markdown("""
    <style>
        body {
            background-color: #fef6fb;
        }
        .main {
            background-color: #fef6fb;
        }
        .stButton>button {
            background-color: #d8f3dc;
            color: black;
            border-radius: 8px;
        }
        .stFileUploader>div>div {
            background-color: #fcd5ce;
            color: black;
            border-radius: 8px;
        }
        .job-card {
            background-color: #fcefee;
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem;
            box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.05);
        }
    </style>
""", unsafe_allow_html=True)


st.title("\U0001F4BC AI Job Recommender")
st.subheader("Upload your resume to find best-matching tech roles")


uploaded_file = st.file_uploader("Upload your Resume (PDF only)", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Extracting text from resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    jobs_df = load_jobs()
    recommendations = recommend_jobs(resume_text, jobs_df, top_n=4)

    st.markdown("---")
    st.header("\U0001F4CA Recommended Roles")

    cols = st.columns(2)
    colors = ["#f9dcc4", "#d0f4de", "#dfe7fd", "#fde2e4"]
    illustrations = {
        "Data Scientist": "https://cdn-icons-png.flaticon.com/512/4344/4344874.png",
        "Frontend Developer": "https://cdn-icons-png.flaticon.com/512/1006/1006771.png",
        "Backend Developer": "https://cdn-icons-png.flaticon.com/512/2721/2721290.png",
        "ML Engineer": "https://cdn-icons-png.flaticon.com/512/977/977597.png",
        "Product Manager": "https://cdn-icons-png.flaticon.com/512/4228/4228703.png"
    }

    for i, (title, desc, score) in enumerate(recommendations):
        col = cols[i % 2]
        with col:
            st.markdown(f"""
                <div class="job-card" style="background-color:{colors[i % len(colors)]}">
                    <h4>{title}</h4>
                    <img src="{illustrations.get(title, '')}" width="60" style="margin-bottom: 10px" />
                    <p>{desc}</p>
                    <b>Match Score:</b> {round(score * 100, 2)}%
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<center>Made with ❤️ by Sai Sree Peruboyina </center>", unsafe_allow_html=True)
else:
    st.info("Please upload a PDF resume to get recommendations.")
