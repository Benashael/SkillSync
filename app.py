import streamlit as st
import spacy
from PyPDF2 import PdfReader
import re
import matplotlib.pyplot as plt

# Load NLP Model
nlp = spacy.load("en_core_web_sm")

# Predefined job categories and associated skills
CATEGORIES = {
    "Data Science": ["Python", "Machine Learning", "Data Analysis", "SQL"],
    "Web Development": ["HTML", "CSS", "JavaScript", "React", "Node.js"],
    "Mobile Development": ["Kotlin", "Swift", "React Native", "Flutter"],
    "Cybersecurity": ["Network Security", "Penetration Testing", "Risk Assessment", "Cryptography"],
    "Digital Marketing": ["SEO", "Google Analytics", "Content Marketing", "PPC"],
    "Product Management": ["Agile", "Scrum", "Roadmap Planning", "Stakeholder Management"],
    "UI/UX Design": ["Figma", "Sketch", "Wireframing", "Prototyping"],
    "Cloud Computing": ["AWS", "Azure", "Google Cloud", "DevOps"],
    "AI/ML Engineering": ["Deep Learning", "NLP", "TensorFlow", "PyTorch"],
    "Business Analysis": ["Requirements Gathering", "Process Mapping", "Stakeholder Communication"],
    "Finance": ["Budgeting", "Forecasting", "Financial Modeling", "Risk Analysis"],
    "Healthcare IT": ["EHR", "HIPAA Compliance", "Medical Imaging", "Telemedicine"],
    "Game Development": ["Unity", "Unreal Engine", "C#", "3D Modeling"],
    "E-commerce": ["Shopify", "Magento", "Inventory Management", "Customer Retention"],
    "Operations Management": ["Six Sigma", "Supply Chain Management", "Logistics", "Lean"],
}

# Mapped terms for short forms
KEYWORD_MAPPINGS = {
    "Machine Learning": ["ML", "machine learning", "machine learnin", "m/l", "machine-learning", "ml algorithms"],
    "Search Engine Optimization": ["SEO", "search optimization", "search engine optimization", "seo strategy", "seo techniques", "site optimization"],
    "Data Analysis": ["data analytics", "analysis", "data analysis", "data interpretation", "analyzing data", "data insights"],
    "JavaScript": ["JS", "javascript", "java script", "js frameworks", "js programming", "javascript coding"],
    "Natural Language Processing": ["NLP", "text processing", "natural lang proc", "nlp models", "language processing", "natural-language-processing"],
    "Penetration Testing": ["Pentest", "security testing", "penetration test", "vulnerability assessment", "pentesting", "ethical hacking"],
    "Python": ["py", "python programming", "python scripting", "python lang", "python code", "pythonic"],
    "SQL": ["structured query language", "sql queries", "database querying", "sql scripting", "sql commands", "relational database"],
    "Deep Learning": ["DL", "deep-learning", "deep neural networks", "deep nn", "dl algorithms", "deep neural net"],
    "Data Visualization": ["data viz", "data visualization", "charts", "graphs", "dashboards", "visualizing data"],
    "Project Management": ["PM", "project mgr", "project handling", "proj mgmt", "project coordination", "project leadership"],
    "Agile": ["scrum", "agile methodology", "agile framework", "agile processes", "agile project management", "agile software development"],
    "Cloud Computing": ["cloud infra", "cloud infrastructure", "cloud services", "aws", "azure", "gcp"],
    "UI/UX Design": ["user interface design", "ux design", "user experience", "ui/ux", "interface design", "ux/ui"],
    "Mobile Development": ["mobile dev", "app dev", "mobile app development", "mobile programming", "app creation", "native apps"],
    "Cybersecurity": ["network security", "cyber security", "cybersec", "information security", "infosec", "cyber protection"],
    "SEO": ["seo", "search engine opt", "website optimization", "seo marketing", "seo campaigns", "seo strategies"],
    "Artificial Intelligence": ["AI", "artificial intelligence", "ai models", "ai techniques", "machine intelligence", "artificial-intelligence"],
    "Data Engineering": ["data engg", "data pipelines", "data engineering", "etl processes", "data processing", "data integration"],
    "Big Data": ["bigdata", "big-data", "data lakes", "hadoop", "spark", "big data technologies"]
}

# Function to clean and normalize text
def clean_text(text):
    text = re.sub(r"\s+", " ", text)  # Remove extra spaces
    text = re.sub(r"[^\w\s]", "", text)  # Remove special characters
    return text.lower()

# Normalize keywords
def normalize_keywords(keywords):
    normalized = []
    for keyword in keywords:
        normalized.append(keyword.lower())
        if keyword in KEYWORD_MAPPINGS:
            normalized.extend([kw.lower() for kw in KEYWORD_MAPPINGS[keyword]])
    return list(set(normalized))

# Extract text from PDF
def extract_text_from_pdf(uploaded_file):
    try:
        reader = PdfReader(uploaded_file)
        text = " ".join(page.extract_text() for page in reader.pages)
        if not text.strip():
            raise ValueError("No readable text found in the resume.")
        return text
    except Exception as e:
        raise ValueError(f"Error reading PDF: {e}")

# Extract keywords
def extract_keywords(text):
    doc = nlp(text)
    return [token.text for token in doc if token.is_alpha and not token.is_stop]

# Calculate match score
def calculate_match_score(resume_keywords, job_keywords, critical_skills):
    matched_keywords = [word for word in resume_keywords if word in job_keywords]
    critical_matches = [word for word in matched_keywords if word in critical_skills]
    score = ((len(matched_keywords) / len(job_keywords)) * 7 if job_keywords else 0) + \
            ((len(critical_matches) / len(critical_skills)) * 3 if critical_skills else 0)
    return score, matched_keywords, critical_matches

# Visualize results
def visualize_keywords(matched, unmatched):
    plt.figure(figsize=(6, 4))
    plt.bar(["Matched", "Unmatched"], [len(matched), len(unmatched)], color=["green", "red"])
    plt.title("Keyword Match Results")
    st.pyplot(plt)

# Streamlit App
st.title("🚀 Enhanced Resume Analyzer & Job Matchmaker")
st.subheader("Analyze your resume and match it with job descriptions.")

# Job category selection
job_category = st.selectbox("📂 Select Job Category", options=["Select"] + list(CATEGORIES.keys()))

# Job description input
job_description = st.text_area("📝 Paste the Job Description (optional)", height=150, placeholder="E.g., Requirements: Python, ML, SQL")

# Resume upload
uploaded_file = st.file_uploader("📄 Upload Your Resume (PDF)", type=["pdf"])

# Analyze button
if st.button("Analyze Resume"):
    try:
        if job_category == "Select" and not job_description.strip():
            raise ValueError("Please select a job category or provide a job description.")

        # Get job keywords
        job_keywords = []
        if job_description.strip():
            job_keywords = extract_keywords(clean_text(job_description))
        elif job_category != "Select":
            job_keywords = CATEGORIES[job_category]
        
        job_keywords = normalize_keywords(job_keywords)

        st.write("### Extracted Job Keywords 📝")
        st.write(job_keywords)

        # Resume processing
        if uploaded_file:
            resume_text = extract_text_from_pdf(uploaded_file)
            resume_keywords = normalize_keywords(extract_keywords(clean_text(resume_text)))

            st.write("### Extracted Resume Keywords 📄")
            st.write(resume_keywords)

            # Match calculation
            critical_skills = job_keywords[:3]  # Take first 3 as critical
            score, matched_keywords, critical_matches = calculate_match_score(resume_keywords, job_keywords, critical_skills)

            st.write(f"### Match Score: **{score:.2f}/10** 🎯")
            st.success("✅ Strong match!" if score > 7 else "🟡 Moderate match; needs improvement." if score > 5 else "❌ Significant gaps detected.")

            unmatched_keywords = [word for word in job_keywords if word not in matched_keywords]
            st.write("**Matched Keywords:**", matched_keywords)
            st.write("**Unmatched Keywords:**", unmatched_keywords)

            if unmatched_keywords:
                st.warning("🔍 Missing keywords in your resume:")
                st.write(unmatched_keywords)

            visualize_keywords(matched_keywords, unmatched_keywords)
        else:
            raise ValueError("Please upload your resume.")
    except ValueError as ve:
        st.error(str(ve))
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
