import pandas as pd
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def load_jobs():
    return pd.read_csv("sample_jobs.csv")  # Contains job titles & descriptions

def recommend_jobs(resume_text, jobs_df, top_n=3):
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    job_embeddings = model.encode(jobs_df['description'].tolist(), convert_to_tensor=True)

    scores = util.cos_sim(resume_embedding, job_embeddings)[0]
    top_results = scores.argsort(descending=True)[:top_n]

    recommendations = []
    for idx in top_results:
        job = jobs_df.iloc[int(idx)]
        recommendations.append((job['title'], job['description'], float(scores[int(idx)])))
    return recommendations
