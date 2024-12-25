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
    "Communication": ["public speaking", "presentation skills", "writing", "verbal communication", "interpersonal skills"],
    "Teamwork": ["collaboration", "team player", "cross-functional collaboration", "working with teams", "team coordination"],
    "Problem Solving": ["critical thinking", "problem solving", "analytical thinking", "troubleshooting", "solution-oriented"],
    "Adaptability": ["flexibility", "adaptability", "open to change", "quick learner", "resilience", "work under pressure"],
    "Time Management": ["time management", "prioritization", "task management", "deadline driven", "multitasking", "efficiency"],
    "Creativity": ["innovation", "creative thinking", "idea generation", "design thinking", "out-of-the-box thinking"],
    "Microsoft Word": ["microsoft word", "word processing", "document formatting", "creating reports", "word documents"],
    "Microsoft Excel": ["microsoft excel", "data analysis", "spreadsheet", "pivot tables", "formulas", "excel macros"],
    "Microsoft PowerPoint": ["microsoft powerpoint", "presentation slides", "ppt", "slide design", "powerpoint presentations"],
    "Microsoft Outlook": ["microsoft outlook", "email communication", "outlook calendar", "meeting scheduling", "email management"],
    "Microsoft Access": ["microsoft access", "database management", "queries", "relational databases", "data entry"],
    "LMS Administration": ["lms", "learning management system", "training support"],
    "Microsoft Office": ["word", "excel", "powerpoint"],
    "Data Science": ["data science", "data scientist", "data-driven insights", "data analysis models", "data research"],
    "Graphic Design": ["graphic design", "photoshop", "illustrator", "adobe creative suite", "design concepts"],
    "Web Development": ["web dev", "website development", "frontend coding", "backend development", "web programming"],
    "Internet of Things": ["IoT", "smart devices", "internet of things", "iot technologies", "connected systems"],
    "Robotic Process Automation": ["RPA", "robotic automation", "automation bots", "process automation", "rpa tools"],
    "Game Development": ["game dev", "game programming", "unity", "unreal engine", "game design"],
    "Augmented Reality": ["AR", "augmented reality", "mixed reality", "ar design", "ar applications"],
    "Virtual Reality": ["VR", "virtual reality", "vr development", "virtual experiences", "immersive tech"],
    "Business Analysis": ["business analytics", "requirements gathering", "business needs analysis", "BA role"],
    "Operations Management": ["ops management", "operations efficiency", "supply chain", "logistics", "ops planning"],
    "Technical Writing": ["tech writing", "documentation", "manual writing", "technical authoring", "content creation"],
    "Digital Transformation": ["digital strategy", "digital transformation initiatives", "business digitization"],
    "Human Resources": ["HR", "recruitment", "talent management", "employee relations", "hr processes"],
    "Content Marketing": ["content strategy", "blogging", "content creation", "social media posts", "content marketing"],
    "Email Marketing": ["email campaigns", "email strategy", "drip campaigns", "email funnels", "mail automation"],
    "IT Support": ["tech support", "it troubleshooting", "desktop support", "helpdesk", "technical assistance"],
    "Social Media Management": ["social platforms", "scheduling posts", "content curation", "social engagement"],
    "E-commerce Management": ["online store management", "product listing", "inventory management", "ecommerce analytics"],
    "Financial Analysis": ["financial modeling", "investment analysis", "risk assessment", "financial reporting"],
    "Supply Chain Management": ["logistics management", "warehouse optimization", "supply chain processes"],
    "Customer Service": ["customer support", "client relations", "customer care", "support resolution"],
    "Cloud Architecture": ["cloud solutions", "cloud architecture design", "cloud scaling"],
    "Network Administration": ["network setup", "IT infrastructure", "network security"],
    "Data Warehousing": ["data lake", "ETL tools", "database optimization", "warehouse solutions"],
    "Database Administration": ["db admin", "database servers", "SQL tuning", "database backup"],
    "AI Ethics": ["AI fairness", "algorithmic transparency", "responsible AI"],
    "UI Design": ["interface design principles", "prototyping", "user testing"],
    "UX Research": ["user behavior analysis", "journey mapping", "usability testing"],
    "Mobile UI Design": ["responsive mobile design", "mobile-first", "touch interface design"],
    "Embedded Systems": ["microcontrollers", "embedded programming", "real-time systems"],
    "Digital Forensics": ["cyber investigations", "digital evidence", "incident analysis"],
    "Risk Management": ["risk assessment", "mitigation strategies", "compliance risks"],
    "DevSecOps": ["secure devops", "security pipelines", "devops compliance"],
    "3D Modeling": ["3d rendering", "model design", "maya", "blender"],
    "Video Editing": ["video post-production", "premiere pro", "final cut pro", "video content creation"],
    "Audio Engineering": ["sound mixing", "audio production", "studio recording"],
    "Renewable Energy": ["solar tech", "green energy", "wind turbine tech", "sustainability projects"],
    "Event Management": ["event planning", "conference logistics", "event marketing"],
    "Legal Compliance": ["regulatory compliance", "legal frameworks", "policy adherence"],
    "Data Security": ["data protection", "information security measures", "data encryption"],
    "Hardware Design": ["PCB design", "hardware testing", "circuit simulation"],
    "Quantum Computing": ["qubits", "quantum algorithms", "quantum programming"],
    "Mathematical Modeling": ["numerical simulations", "optimization problems", "mathematical proofs"],
    "ERP Systems": ["enterprise resource planning", "SAP ERP", "oracle ERP", "workflow automation"],
    "CRM Systems": ["salesforce CRM", "customer relations tools", "CRM integrations"],
    "API Development": ["REST API", "SOAP API", "API integrations"],
    "Ethical Hacking": ["penetration testing certifications", "vulnerability exploitation"],
    "Mobile Security": ["secure apps", "mobile device management", "msecure practices"],
    "System Design": ["scalable architectures", "design diagrams", "system workflows"],
    "SaaS Solutions": ["subscription platforms", "software as a service", "SaaS optimization"],
    "Biometric Technology": ["facial recognition", "fingerprint systems", "biometric auth"],
    "Data Ethics": ["data anonymization", "privacy ethics", "ethical data use"],
    "Personal Branding": ["linkedin optimization", "professional profiles", "online visibility"],
    "Cryptography": ["data encryption techniques", "secure communications", "cryptanalysis"],
    "Drone Technology": ["aerial robotics", "drone operations", "unmanned vehicles"],
    "E-Learning": ["course creation", "online teaching", "virtual classrooms"],
    "Cross-Platform Development": ["flutter", "react native", "cross-platform apps"],
    "Data Archiving": ["long-term storage", "archive solutions", "data lifecycle management"],
    "Remote Sensing": ["satellite imagery", "geospatial analysis", "remote sensing tech"],
    "Biomedical Engineering": ["bioinformatics", "medical imaging", "healthcare innovations"],
    "Climate Modeling": ["weather predictions", "climate simulations", "earth systems analysis"],
    "Robotics": ["autonomous robots", "mechanical systems", "robot control software"],
    "Crowdfunding": ["fundraising campaigns", "kickstarter", "indiegogo marketing"],
    "Negotiation": ["contract negotiation", "deal closure", "conflict resolution"],
    "Organizational Behavior": ["team dynamics", "corporate culture", "leadership impact"],
    "Storyboarding": ["narrative planning", "animation storyboards", "visual scripts"],
    "Design Thinking": ["empathize ideate prototype", "innovation strategy", "design processes"],
    "Health Informatics": ["electronic health records", "medical data systems", "patient management tech"],
    "Bioinformatics": ["genomic data", "protein analysis", "bioinfo tools"],
    "Agricultural Technology": ["precision farming", "agribots", "soil data analysis"],
    "Digital Wallets": ["payment systems", "mobile wallets", "digital payments"],
    "Smart Cities": ["urban IoT", "smart grids", "smart mobility"],
    "Cryptocurrency": ["crypto trading", "bitcoin", "blockchain finance"],
    "Creative Writing": ["fiction writing", "scriptwriting", "creative content"],
    "Public Relations": ["media relations", "press releases", "PR campaigns"],
    "Space Technologies": ["satellite systems", "space exploration", "aerospace engineering"],
    "3D Printing": ["additive manufacturing", "printing tech", "material science"],
    "Open Source Contributions": ["github projects", "open-source codebases", "community software"],
    "Statistical Modeling": ["regression models", "time series analysis", "statistical inference"],
    "Ethics and Compliance": ["ethical policies", "corporate compliance", "values alignment"],
    "Web Security": ["anti-hacking", "secure protocols", "site hardening"],
    "Digital Branding": ["brand management", "online identity", "digital campaigns"],
    "Digital Twins": ["virtual replicas", "simulation models", "digital mapping"],
    "UX Strategy": ["user-centered design", "experience optimization", "strategy alignment"],
    "AI in Healthcare": ["predictive healthcare", "ai diagnostics", "medtech innovation"],
    "Bioengineering": ["biotech", "bioengineering processes", "biological systems", "biomaterials", "biosensors"],
    "Knowledge Management": ["organizational knowledge", "KM tools", "knowledge sharing", "knowledge retention"],
    "Digital Advertising": ["online ads", "ad targeting", "ppc campaigns", "digital ad strategies"],
    "Industrial Automation": ["factory automation", "industrial robots", "process control", "PLC programming"],
    "Sustainability": ["eco-friendly practices", "green technologies", "sustainability metrics", "carbon footprint reduction"],
    "Energy Management": ["energy optimization", "renewable resources", "power distribution", "smart grids"],
    "Customer Experience": ["CX", "customer journey mapping", "user experience improvement", "customer touchpoints"],
    "Market Research": ["consumer insights", "competitive analysis", "market trends", "survey methodologies"],
    "User Research": ["user feedback", "persona development", "UX insights", "research methodologies"],
    "Predictive Analytics": ["trend forecasting", "data predictions", "predictive modeling", "forecasting tools"],
    "Knowledge Graphs": ["semantic graphs", "data relationships", "ontology building", "linked data"],
    "Edge Computing": ["fog computing", "distributed systems", "local data processing", "edge devices"],
    "Hybrid Cloud": ["cloud combination", "public-private cloud", "hybrid IT solutions", "hybrid infrastructure"],
    "Open Data": ["data democratization", "public datasets", "open access information", "data transparency"],
    "Social Impact Analysis": ["community initiatives", "impact metrics", "social project evaluations"],
    "Animation": ["2D animation", "3D animation", "motion graphics", "animation workflows"],
    "Corporate Training": ["employee development", "training programs", "workshop facilitation"],
    "Smart Devices": ["IoT gadgets", "connected tech", "home automation", "smart system integration"],
    "Health Monitoring": ["wearable tech", "health sensors", "patient monitoring", "fitness trackers"],
    "Server Administration": ["server maintenance", "hosting management", "system performance", "server-side support"],
    "Environmental Science": ["climate studies", "biodiversity research", "eco systems", "sustainability science"],
    "Ethnographic Studies": ["cultural insights", "field research", "human behavior analysis"],
    "Legal Tech": ["contract automation", "legal research tools", "case management software"],
    "Quantum Algorithms": ["quantum programming", "shor's algorithm", "quantum computing models"],
    "Crowd Management": ["public safety", "event security", "crowd analytics", "large-scale coordination"],
    "AI-Powered Chatbots": ["conversational AI", "customer service bots", "virtual assistants"],
    "Media Production": ["content editing", "studio operations", "multimedia creation"],
    "Climate Adaptation": ["resilience planning", "climate risk assessment", "adaptive measures"],
    "E-Waste Management": ["electronics recycling", "waste minimization", "eco disposal"],
    "RegTech": ["regulatory tech", "compliance automation", "legal risk management"],
    "Product Lifecycle Management": ["PLM", "design-to-market", "lifecycle optimization"],
    "Agritech": ["farming tech", "smart agriculture", "crop monitoring", "farm optimization"],
    "Behavioral Science": ["human behavior patterns", "decision analysis", "behavior modeling"],
    "Language Translation": ["linguistic services", "automated translation", "multilingual communication"],
    "Digital Twins": ["real-time simulation", "virtual replicas", "digital modeling"],
    "Emotional Intelligence": ["EQ", "empathy building", "emotional awareness"],
    "Smart Wearables": ["wearable tech", "smart health devices", "fitness bands"],
    "Space Exploration": ["orbital systems", "planetary research", "aerospace innovations"],
    "Data Privacy": ["GDPR compliance", "privacy by design", "data protection laws"],
    "Speech Processing": ["voice recognition", "speech-to-text", "acoustic analysis"],
    "Text Summarization": ["extractive summarization", "abstractive summarization", "text compression"],
    "Knowledge Representation": ["logical reasoning", "ontology creation", "semantic frameworks"],
    "Bioinformatics Algorithms": ["genomic sequence", "phylogenetic trees", "biological computation"],
    "Robotic Surgery": ["automated procedures", "surgical robotics", "minimally invasive tech"],
    "Digital Storytelling": ["interactive narratives", "multimedia stories", "virtual storytelling"],
    "IoT Security": ["device protection", "IoT encryption", "network integrity"],
    "API Security": ["token management", "secure endpoints", "API gateway protection"],
    "Low-Code Development": ["drag-and-drop coding", "visual programming", "rapid app development"],
    "Game Mechanics": ["reward systems", "level design", "player interaction"],
    "Data Compression": ["file size reduction", "lossless compression", "encoding techniques"],
    "Image Processing": ["pixel manipulation", "filter design", "image segmentation"],
    "Energy Storage": ["battery tech", "grid storage", "power cells"],
    "Vehicle Telematics": ["fleet management", "vehicle tracking", "telematic systems"],
    "Performance Optimization": ["process improvement", "speed enhancement", "resource tuning"],
    "Employee Engagement": ["workforce satisfaction", "motivation strategies", "engagement metrics"],
    "Recruitment Technology": ["AI hiring tools", "resume screening", "job matching"],
    "Fraud Detection": ["anomaly spotting", "risk algorithms", "transaction monitoring"],
    "Crisis Management": ["contingency planning", "risk mitigation", "emergency response"],
    "Data Provenance": ["source tracking", "data lineage", "traceability"],
    "Algorithm Development": ["problem-solving algorithms", "optimization techniques"],
    "Oceanography": ["marine studies", "ocean modeling", "underwater exploration"],
    "Wearable Robotics": ["exoskeleton tech", "assistive devices", "robotic wearables"],
    "Ethical HCI": ["user ethics", "human-centered computing", "design responsibility"],
    "Remote Collaboration": ["virtual teams", "online brainstorming", "remote work tools"],
    "Scripting Languages": ["bash scripting", "perl programming", "automation scripts"],
    "Mobile AR": ["augmented mobile apps", "AR gaming", "AR filters"],
    "Assistive Technology": ["disability tech", "assistive devices", "accessible solutions"],
    "Cross-Cultural Training": ["cultural sensitivity", "global business training", "cross-cultural dynamics"],
    "Data Augmentation": ["synthetic data", "training data enhancement", "augmentation techniques"],
    "Microservices Architecture": ["service-oriented architecture", "SOA", "microservices development", "containerized apps"],
    "Renewable Energy": ["solar energy", "wind power", "green energy", "sustainable energy systems"],
    "Digital Marketing Analytics": ["campaign metrics", "marketing KPIs", "ROI tracking", "conversion analysis"],
    "Computer Vision": ["image recognition", "object detection", "CV algorithms", "vision systems"],
    "Human-Computer Interaction": ["HCI design", "user interfaces", "interaction design", "user experience studies"],
    "Gene Editing": ["CRISPR", "genetic modification", "biotech engineering", "gene therapy"],
    "Video Production": ["film editing", "video scripting", "cinematography", "media editing"],
    "Gamification": ["engagement strategies", "game-like experiences", "behavioral incentives"],
    "Supply Chain Optimization": ["logistics management", "inventory planning", "SCM", "demand forecasting"],
    "e-Learning Development": ["online course creation", "instructional design", "e-learning platforms"],
    "Data Lakes": ["big data storage", "data lake architecture", "unstructured data handling"],
    "Digital Twins for IoT": ["virtual IoT devices", "real-time modeling", "digital representation"],
    "5G Technology": ["next-gen networks", "5G connectivity", "ultra-fast broadband", "wireless tech"],
    "Autonomous Vehicles": ["self-driving cars", "vehicle autonomy", "ADAS", "driverless systems"],
    "Kubernetes Orchestration": ["K8s", "container management", "cluster orchestration"],
    "Data Monetization": ["data-driven revenue", "data as a product", "commercializing data"],
    "Neuro-Linguistic Programming": ["NLP therapy", "mindset transformation", "communication techniques"],
    "Chatbot Development": ["virtual agents", "AI conversations", "interactive bots"],
    "Customer Retention": ["loyalty programs", "churn reduction", "client engagement strategies"],
    "Knowledge-Based Systems": ["expert systems", "decision support", "rule-based AI"],
    "Wearable Medical Devices": ["health trackers", "biometric monitoring", "wearable diagnostics"],
    "Hybrid Work Models": ["remote and onsite", "flexible work", "hybrid workforce strategies"],
    "AI in Healthcare": ["medical imaging AI", "predictive health analytics", "digital diagnosis"],
    "Smart Grids": ["intelligent energy networks", "grid optimization", "smart energy systems"],
    "Automated Quality Control": ["QA automation", "smart testing systems", "machine-driven QC"],
    "Personal Finance Management": ["budget tracking", "expense management", "financial planning tools"],
    "Voice Assistants": ["virtual assistants", "voice AI", "voice-activated tech"],
    "Predictive Maintenance": ["equipment monitoring", "failure prediction", "maintenance analytics"],
    "Generative AI": ["creative AI", "content generation", "AI-generated art"],
    "Sentiment Analysis": ["opinion mining", "customer sentiment", "text-based emotion analysis"],
    "Natural Disaster Management": ["disaster prediction", "emergency systems", "crisis response tech"],
    "Information Retrieval": ["search algorithms", "data fetching", "indexing systems"],
    "Cloud Security": ["data protection in cloud", "cloud access control", "cloud encryption"],
    "AI Ethics": ["responsible AI", "bias mitigation", "ethical decision-making in AI"],
    "Social Media Management": ["content scheduling", "social media campaigns", "SM analytics"],
    "IoT Analytics": ["device data analysis", "IoT insights", "connected device stats"],
    "Synthetic Biology": ["bioengineered systems", "synthetic organisms", "genome synthesis"],
    "Predictive Text": ["autocomplete systems", "AI typing", "text prediction"],
    "AI-Powered Personalization": ["custom user experiences", "personalized recommendations", "AI-driven customization"],
    "Data Labeling": ["annotation tools", "data tagging", "training data prep"],
    "Home Automation": ["smart home tech", "connected living", "home IoT devices"],
    "Advanced Robotics": ["robotics AI", "intelligent automation", "robot dynamics"],
    "E-Commerce Optimization": ["online sales strategies", "cart abandonment reduction", "conversion rate optimization"],
    "Workflow Automation": ["process automation", "task orchestration", "workflow tools"],
    "Design Systems": ["UI frameworks", "design libraries", "component-based design"],
    "Streaming Media": ["live streaming", "OTT platforms", "video on demand"],
    "Ethical Hacking": ["penetration testing", "network defense", "ethical cybersecurity"],
    "Robotics Process Automation": ["RPA bots", "task automation", "workflow efficiency"],
    "Digital Watermarking": ["content protection", "media ownership", "digital rights"],
    "Crowdsourcing": ["distributed problem-solving", "crowd collaboration", "open innovation"],
    "Virtual Events": ["online conferencing", "digital summits", "virtual meetups"],
    "Real-Time Analytics": ["instant insights", "live data processing", "real-time dashboards"],
    "Mobile Wallets": ["digital payments", "contactless transactions", "e-wallets"],
    "Affective Computing": ["emotion AI", "sentiment-aware systems", "human-like interactions"],
    "Cyber Threat Intelligence": ["threat hunting", "cyber risk analysis", "malware detection"],
    "Zero Trust Security": ["access verification", "identity-first security", "ZT architecture"],
    "Customer Onboarding": ["client activation", "welcome programs", "onboarding strategies"],
    "Biometrics": ["fingerprint recognition", "facial authentication", "biometric security"],
    "SaaS Development": ["cloud applications", "software as a service", "subscription models"],
    "AI-Powered Creativity": ["creative assistants", "AI design tools", "generative design"],
    "Digital Therapeutics": ["health apps", "digital care programs", "behavioral health tech"],
    "Account Management": ["key account management", "client account handling", "account relationships"],
    "Business Development": ["BD", "sales growth", "new client acquisition", "expansion strategies"],
    "Sales Enablement": ["sales support", "enablement tools", "sales productivity"],
    "Client Relationship Management": ["CRM", "customer relationships", "client interactions", "relationship building"],
    "Lead Generation": ["prospecting", "lead identification", "new business leads"],
    "Sales Strategy": ["sales planning", "strategic selling", "revenue growth plans"],
    "Customer Retention": ["client loyalty", "retention programs", "renewals"],
    "Pipeline Management": ["sales pipeline", "opportunity tracking", "deal progression"],
    "Cross-Selling": ["additional sales", "product upsell", "client upsell opportunities"],
    "Client Onboarding": ["welcome process", "initial engagement", "onboarding support"],
    "B2B Sales": ["business-to-business sales", "corporate sales", "enterprise deals"],
    "B2C Sales": ["retail sales", "consumer engagement", "direct selling"],
    "Sales Forecasting": ["revenue prediction", "sales trends", "performance estimation"],
    "Cold Calling": ["outbound calls", "prospecting calls", "lead cold outreach"],
    "Customer Feedback Analysis": ["client surveys", "customer insights", "feedback review"],
    "Sales Presentations": ["pitch decks", "client proposals", "sales demonstrations"],
    "Negotiation Skills": ["deal negotiation", "contract finalization", "sales closures"],
    "Sales Reporting": ["performance metrics", "sales data analysis", "revenue reports"],
    "Upselling Strategies": ["upsell techniques", "premium sales", "product upgrades"],
    "Customer Complaint Handling": ["issue resolution", "escalation management", "client grievances"],
    "Retail Management": ["store sales", "in-store promotions", "retail strategy"],
    "Territory Management": ["regional sales", "territory planning", "area coverage"],
    "Market Research for Sales": ["competitor analysis", "market trends", "industry insights"],
    "Sales Incentives Planning": ["commission structures", "bonus plans", "sales motivation"],
    "Inside Sales": ["remote sales", "virtual client interactions", "phone-based selling"],
    "Field Sales": ["door-to-door sales", "on-site client visits", "outdoor sales"],
    "Channel Sales": ["partner networks", "distributor management", "reseller programs"],
    "After-Sales Service": ["customer support", "service follow-up", "post-sales care"],
    "Sales Training": ["team coaching", "sales workshops", "skill development"],
    "Customer Advocacy": ["client champions", "customer reference programs", "client success stories"],
    "Key Performance Indicators (KPIs)": ["sales KPIs", "performance tracking", "goal achievement"],
    "Proposal Writing": ["client proposals", "business bids", "sales documentation"],
    "Loyalty Programs": ["customer rewards", "membership programs", "repeat business incentives"],
    "CRM Software": ["customer management tools", "salesforce", "hubspot", "zoho CRM"],
    "Product Demos": ["live demonstrations", "feature presentations", "trial sessions"],
    "Contract Negotiation": ["deal terms", "agreement finalization", "contract drafting"],
    "Sales Funnel Optimization": ["conversion rate", "sales journey", "lead nurturing"],
    "Event Sales": ["exhibition sales", "trade show leads", "event-based promotions"],
    "Client Escalation Handling": ["issue escalation", "critical client cases", "problem resolution"],
    "Sales Automation Tools": ["sales tech", "pipeline automation", "sales software"],
    "Consultative Selling": ["problem-solving sales", "solution-driven selling", "consultative approaches"],
    "Customer Journey Mapping": ["client lifecycle", "user journey", "customer path analysis"],
    "Proposal Negotiation": ["proposal approval", "deal crafting", "terms negotiation"],
    "Value-Based Selling": ["ROI selling", "customer value creation", "benefit-driven sales"],
    "Client Retention Strategies": ["long-term client relationships", "loyalty building", "repeat business"],
    "Social Selling": ["sales via social media", "LinkedIn prospecting", "social engagement"],
    "Client Portfolio Management": ["client categorization", "portfolio optimization", "high-value clients"],
    "Order Fulfillment": ["order tracking", "delivery coordination", "sales order execution"],
    "Brand Ambassador Programs": ["sales advocacy", "client representation", "customer promoters"]
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

BASE_CATEGORY = {
    "Base Category": [
        "sales",
        "ground staff",
        "business development associate",
        "graduate trainee",
        "customer service",
        "client handling",
        "field work",
        "operations",
        "onboarding",
        "trainee",
        "intern",
        "entry level",
        "junior associate",
        "support staff",
        "administration",
        "team assistant",
        "general staff"
    ]
}

# Quality Score Calculation (50% Weightage)
def score_quality(resume_text):
    score = 0
    # Check formatting (e.g., headers, one-page limit)
    headers = ["education", "skills", "experience", "certifications", "summary", "achievements"]
    for header in headers:
        if header in resume_text.lower():
            score += 2  # Assign points for each proper header

   # Check strong action verbs (eliminates duplicates)
    score += sum(2 for verb in set(STRONG_ACTION_VERBS) if verb.lower() in resume_text.lower())
    
    # Check quantifiers (eliminates duplicates)
    score += sum(2 for quantifier in set(QUANTIFIERS) if quantifier.lower() in resume_text.lower())

    # Check length (favor resumes with 300 to 750 words)
    resume_length = len(resume_text.split())  # Define the resume length
    if 300 <= resume_length <= 750:
        score += 20  # Award more points for resumes of this length
    elif 150 <= resume_length <= 299:
        score += 10
    else:
        score += 5

    return min(score, 49)  # Cap the quality score at 50

# Relevance Score Calculation (45% Weightage)
def score_relevance(resume_text, jd_text):
    # Normalize the texts
    import re
    resume_text = re.sub(r'[^\w\s]', '', resume_text.lower())
    jd_text = re.sub(r'[^\w\s]', '', jd_text.lower())
    
    matching_words = set()
    jd_keywords = set()  # Store keywords found in JD

    # Match keywords in JD
    for keyword, variations in KEYWORD_MAPPINGS.items():
        for variation in variations:
            if variation in jd_text:
                jd_keywords.add(keyword)  # Add to JD keywords
    
    # Match keywords in both JD and resume
    for keyword in jd_keywords:
        for variation in KEYWORD_MAPPINGS[keyword]:
            if variation in resume_text:
                matching_words.add(keyword)
    
    # Calculate relevance score
    if jd_keywords:  # Avoid division by zero
        relevance_score = min(len(matching_words) / len(jd_keywords) * 35, 35)
    elif any(term in jd_text for term in BASE_CATEGORY):  # Check for Base Category terms
        relevance_score = 25  # JD comes under Base Category
    else:
        relevance_score = 0  # No relevant keywords in JD
    
    total_score = 10 + relevance_score  # Add base score of 20
    
    return min(total_score, 43)  # Return matching words and capped score


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

def show_details():
    st.write("### Detailed Breakdown of Your Resume Score")

    # Display Subcategories in Quality Score Calculation
    st.write("#### Content Quality Rating - Subcategories:")
    header_score = 0
    action_verb_score = 0
    quantifier_score = 0
    content_score = 0

    # Check headers
    headers = ["education", "skills", "experience", "certifications", "summary", "achievements"]
    for header in headers:
        if header in resume_text.lower():
            header_score += 2  # Assign points for each proper header

    # Check strong action verbs (eliminates duplicates)
    action_verb_score = sum(2 for verb in set(STRONG_ACTION_VERBS) if verb.lower() in resume_text.lower())
    
    # Check quantifiers (eliminates duplicates)
    quantifier_score = sum(2 for quantifier in set(QUANTIFIERS) if quantifier.lower() in resume_text.lower())

    # Check length (favor resumes with 300 to 750 words)
    resume_length = len(resume_text.split())  # Define the resume length
    if 300 <= resume_length <= 750:
        content_score = 20  # Award more points for resumes of this length
    elif 150 <= resume_length <= 299:
        content_score = 10
    else:
        content_score = 5

    # Write the individual scores using st.write
    st.write("### Detailed Quality Score Breakdown:")
    st.write(f"- **Score for Headers:** {round(header_score, 2)}")
    st.write(f"- **Score for Action Verbs:** {round(action_verb_score, 2)}")
    st.write(f"- **Score for Quantifiers:** {round(quantifier_score, 2)}")
    st.write(f"- **Score for Content (Length):** {round(content_score, 2)}")
    st.write(f"**Total Quality Score:** {min(round(header_score + action_verb_score + quantifier_score + content_score, 2), 49)} / 50")

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
            st.write(f"**Content Quality Rating: {round(quality_score, 2)} / 50**")
            st.write(f"**Job Relevance Assessment: {round(relevance_score, 2)} / 45**")
            st.write(f"**Emerging Skills Index: {round(trending_score, 2)} / 5**")

            show_details()
            
            # Calculate final score (optional for testing purposes)
            final_score = round(quality_score + relevance_score + trending_score, 2)
            st.success(f"**Your final resume score is: {final_score} / 100**")


            if final_score < 70:
                st.info("Aim for a score of 70% or higher for better alignment with the job requirements.")
            else:
                st.success("Great job! Your resume aligns well with the job requirements. Keep it up!")
                
