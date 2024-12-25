import streamlit as st
import docx2txt
from PyPDF2 import PdfReader
from langdetect import detect

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
    "Big Data": ["bigdata", "big-data", "data lakes", "hadoop", "spark", "big data technologies"],
    "DevOps": ["devops", "ci/cd", "continuous integration", "continuous delivery", "docker", "kubernetes"],
    "Blockchain": ["blockchain", "distributed ledger", "cryptocurrency", "ethereum", "smart contracts", "dapps"],
    "Quality Assurance": ["qa", "testing", "quality testing", "automation testing", "manual testing", "bug tracking"],
    "Data Governance": ["data policies", "data compliance", "data stewardship", "data privacy", "data management"],
    "Leadership": ["team management", "mentorship", "decision making", "vision planning", "strategy development"],
    "Communication": ["public speaking", "presentation skills", "writing", "verbal communication", "interpersonal skills"]
}

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
    "DevOps": ["Docker", "Kubernetes", "CI/CD", "Jenkins"],
    "Blockchain": ["Smart Contracts", "Ethereum", "Bitcoin", "Decentralized Apps"],
    "Quality Assurance": ["Automation Testing", "Manual Testing", "Bug Tracking", "Performance Testing"]
}

STRONG_ACTION_VERBS = [
    "Achieved", "Advised", "Analyzed", "Built", "Collaborated", "Conducted", "Created", "Delivered", "Designed", 
    "Developed", "Directed", "Enhanced", "Established", "Executed", "Expanded", "Facilitated", "Generated", 
    "Improved", "Implemented", "Initiated", "Innovated", "Led", "Managed", "Maximized", "Optimized", 
    "Orchestrated", "Planned", "Produced", "Reduced", "Resolved", "Streamlined", "Supervised", "Transformed", 
    "Utilized"
]

QUANTIFIERS = [
    "increased revenue by", "reduced costs by", "improved efficiency by", "generated savings of", "enhanced performance by",
    "achieved growth of", "delivered results with", "surpassed goals by", "completed projects within", "exceeded expectations by"
]

TRENDING_SKILLS = ["AI", "Artificial Intelligence", "Data Science", "Machine Learning", "Microsoft Excel", "PowerPoint", "Word"]

def extract_text(file):
    try:
        if file.type == "application/pdf":
            reader = PdfReader(file)
            text = " ".join(page.extract_text() for page in reader.pages)
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = docx2txt.process(file)
        elif file.type == "text/plain":
            text = file.read().decode("utf-8")
        else:
            return None
        return text.strip()
    except Exception as e:
        return None

def score_quality(resume_text):
    score = 0
    headers = ["education", "skills", "experience", "certifications", "summary", "achievements"]
    for header in headers:
        if header in resume_text.lower():
            score += 5  # Assign points for each proper header

    score += sum(1 for verb in STRONG_ACTION_VERBS if verb.lower() in resume_text.lower())
    score += sum(1 for quantifier in QUANTIFIERS if quantifier.lower() in resume_text.lower())

    if len(resume_text.split()) <= 400:  # Rough estimate for one page
        score += 10

    return min(score, 50)  # Cap the quality score at 50

def score_relevance(resume_text, jd_text):
    matching_words = set()
    for keyword, variations in KEYWORD_MAPPINGS.items():
        for variation in variations:
            if variation in resume_text.lower() and variation in jd_text.lower():
                matching_words.add(keyword)

    return min(len(matching_words) / len(KEYWORD_MAPPINGS) * 100, 45)  # Cap relevance score at 45

def score_trending_skills(resume_text):
    score = sum(1 for skill in TRENDING_SKILLS if skill.lower() in resume_text.lower())
    return min(score * 5, 5)  # Cap trending skills score at 5

def calculate_final_score(resume_text, jd_text):
    quality_score = score_quality(resume_text)
    relevance_score = score_relevance(resume_text, jd_text)
    trending_score = score_trending_skills(resume_text)

    final_score = quality_score + relevance_score + trending_score
    return round(final_score, 2)

def score_resume(resume_text, jd_text):
    resume_words = set(resume_text.lower().split())
    jd_words = set(jd_text.lower().split())
    matching_words = set()
    strong_verbs_score = sum(1 for verb in STRONG_ACTION_VERBS if verb.lower() in resume_text.lower())
    quantifiers_score = sum(1 for quantifier in QUANTIFIERS if quantifier.lower() in resume_text.lower())

    for keyword, variations in KEYWORD_MAPPINGS.items():
        for variation in variations:
            if variation in resume_words and variation in jd_words:
                matching_words.add(keyword)

    score = len(matching_words) / len(KEYWORD_MAPPINGS) * 100
    boost_score = strong_verbs_score * 2 + quantifiers_score * 3
    total_score = min(score + boost_score, 100)
    return round(total_score, 2)

# Streamlit UI
st.title("Resume Scoring Application")
st.write("Upload your resume and job description to get a compatibility score.")

# Upload Resume
resume_file = st.file_uploader("Upload your Resume (PDF, DOCX, TXT):", type=["pdf", "docx", "txt"])

# Upload or Paste JD
jd_input_method = st.radio("How would you like to provide the Job Description?", ["Upload File", "Paste Text"])
if jd_input_method == "Upload File":
    jd_file = st.file_uploader("Upload Job Description (PDF, DOCX, TXT):", type=["pdf", "docx", "txt"])
    jd_text = extract_text(jd_file) if jd_file else None
else:
    jd_text = st.text_area("Paste the Job Description:").strip()

# Process and Score
if st.button("Score My Resume"):
    if not resume_file:
        st.error("Please upload your resume.")
    elif not jd_text:
        st.error("Please provide the job description.")
    else:
        resume_text = extract_text(resume_file)

        if not resume_text:
            st.error("Unable to extract text from the resume. Ensure the format is correct.")
        elif detect(resume_text) != "en" or detect(jd_text) != "en":
            st.error("Both the resume and job description must be in English.")
        else:
            # Calculate the score
            score = score_resume(resume_text, jd_text)
            st.success(f"Your resume's compatibility score with the job description is: {score}%")
            st.info("Aim for a score of 70% or higher for better alignment with the job requirements.")
