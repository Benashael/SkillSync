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
    "increased", "reduced", "improved", "generated", "enhanced", "achieved", "delivered", "surpassed", "completed", "exceeded"
]

TRENDING_SKILLS = [
    "AI", "Artificial Intelligence", "Machine Learning", "ML", "AI Models", "Deep Learning", "DL",
    "Data Science", "Data Analytics", "Data Analysis", "Big Data", "Data Engineering", "Data Mining",
    "Natural Language Processing", "NLP", "Computer Vision", "CV", "Python", "Python Programming", "Python Scripting",
    "R Programming", "TensorFlow", "TF", "PyTorch", "Scikit-learn", "Keras", "Deep Neural Networks", "DNN",
    "Artificial Neural Networks", "ANN", "Neural Networks", "Data Visualization", "Tableau", "Power BI",
    "Microsoft Excel", "Excel", "PowerPoint", "PPT", "Word", "Google Analytics", "Google Sheets", "SQL",
    "Structured Query Language", "NoSQL", "MongoDB", "MySQL", "PostgreSQL", "Oracle", "Hadoop", "Spark",
    "AWS", "Amazon Web Services", "Azure", "Google Cloud", "GCP", "Docker", "Kubernetes", "DevOps", "CI/CD",
    "Git", "Version Control", "Blockchain", "Cryptocurrency", "Ethereum", "Smart Contracts", "Dapps",
    "SEO", "Search Engine Optimization", "SEM", "PPC", "Content Marketing", "Marketing Automation",
    "Agile", "Scrum", "Scrum Master", "Project Management", "Jira", "Kanban", "DevOps", "Scrum Framework"
]


# Quality Score Calculation (50% Weightage)
def score_quality(resume_text):
    score = 0
    # Check formatting (e.g., headers, one-page limit)
    headers = ["education", "skills", "experience", "certifications", "summary", "achievements"]
    for header in headers:
        if header in resume_text.lower():
            score += 3  # Assign points for each proper header

    # Check strong action verbs
    score += sum(3 for verb in STRONG_ACTION_VERBS if verb.lower() in resume_text.lower())

    # Check quantifiers
    score += sum(2 for quantifier in QUANTIFIERS if quantifier.lower() in resume_text.lower())

    # Check length (favor resumes with 300 to 750 words)
    resume_length = len(resume_text.split())  # Define the resume length
    if 250 <= resume_length <= 750:
        score += 20  # Award more points for resumes of this length
    elif 150 <= resume_length <= 249:
        score += 10
    else:
        score += 5

    return min(score, 50)  # Cap the quality score at 50

# Relevance Score Calculation (45% Weightage)
def score_relevance(resume_text, jd_text):
    matching_words = set()
    for keyword, variations in KEYWORD_MAPPINGS.items():
        for variation in variations:
            if variation in resume_text.lower() and variation in jd_text.lower():
                matching_words.add(keyword) 

    # Calculate the relevance score based on matching keywords
    relevance_score = min(len(matching_words) / len(KEYWORD_MAPPINGS) * 100, 45)  # Cap relevance score at 45

    # Set base score as 20 and add the calculated score
    total_score = 20 + relevance_score

    return matching_words, min(total_score, 45)  # Ensure the total score doesn't exceed 45

# Trending Skills Score Calculation (5% Weightage)
def score_trending_skills(resume_text):
    # Convert resume text to lowercase for case-insensitive matching
    resume_text_lower = resume_text.lower()
    
    # Create a set to track skills found in the resume (avoiding duplicates)
    found_skills = set()

    # Check each skill in the trending skills list
    for skill in TRENDING_SKILLS:
        if skill.lower() in resume_text_lower:
            found_skills.add(skill.lower())  # Add to set to avoid duplicates

    # Calculate the score based on the number of unique skills found
    score = len(found_skills) * 0.5  # Each skill adds 0.5 to the score
    return min(score * 5, 5)  # Cap trending skills score at 5


# Final Score Calculation
def calculate_final_score(resume_text, jd_text):
    quality_score = score_quality(resume_text)
    relevance_score = score_relevance(resume_text, jd_text)
    trending_score = score_trending_skills(resume_text)

    final_score = (quality_score * 0.50) + (relevance_score * 0.45) + (trending_score * 0.05)
    return round(final_score, 2)

# Function to extract text from a file
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
            # Calculate individual scores for each category
            quality_score = score_quality(resume_text)
            relevance_score = score_relevance(resume_text, jd_text)
            trending_score = score_trending_skills(resume_text)

            # Show the scores separately
            st.write(f"Quality Score: {quality_score} / 50")
            st.write(f"Relevance Score: {relevance_score} / 45")
            st.write(f"Trending Skills Score: {trending_score} / 5")

            # Calculate final score (optional for testing purposes)
            final_score = quality_score + relevance_score + trending_score
            st.success(f"Your final resume score is: {final_score} / 100")
            st.info("Aim for a score of 70% or higher for better alignment with the job requirements.")
            # Calculate the score
            final_score = calculate_final_score(resume_text, jd_text)
            st.success(f"Your final resume score is: {final_score} / 100")
            st.info("Aim for a score of 70% or higher for better alignment with the job requirements.")
