# 🤖 AI Resume Screening System

An intelligent resume screening system powered by Machine Learning that automatically analyzes resumes, matches them with job descriptions, and provides detailed scoring and skill gap analysis.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.3+-green)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### Core Functionality
- 📤 **Resume Upload** - Support for PDF and DOCX formats
- 🔍 **Text Extraction** - Advanced PDF/DOCX parsing with multiple fallback methods
- 🎯 **Smart Matching** - ML-powered resume-job matching using TF-IDF and cosine similarity
- 📊 **Comprehensive Scoring** - Multi-dimensional scoring system
- 🔧 **Skill Gap Analysis** - Identify matched and missing skills
- 💾 **Database Storage** - SQLite database for all data persistence
- 📈 **Analytics Dashboard** - System-wide analytics and insights

### Scoring Components
- **Skill Match Score** (40% weight) - Required and preferred skills matching
- **Text Similarity Score** (25% weight) - Semantic similarity between resume and job description
- **Experience Score** (20% weight) - Years of experience matching
- **Education Score** (15% weight) - Education level matching

### Intelligent Features
- Automatic candidate information extraction (name, email, phone)
- Experience years detection from resume text
- Education level identification
- 100+ common technical skills recognition
- Recommendation generation (Highly Recommended, Recommended, Maybe, Not Recommended)

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **Flask-SQLAlchemy** - ORM for database
- **scikit-learn** - Machine Learning (TF-IDF, Cosine Similarity)
- **PyPDF2 & pdfplumber** - PDF text extraction
- **python-docx** - DOCX text extraction

### Frontend
- **HTML5/CSS3** - Clean, modern UI
- **Vanilla JavaScript** - No framework dependencies
- **Responsive Design** - Works on all devices

### Database
- **SQLite** - Lightweight, serverless database

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## 🚀 Installation & Setup

### 1. Clone the Repository

\`\`\`bash
git clone https://github.com/rahul700raj/ai-resume-screening-system.git
cd ai-resume-screening-system
\`\`\`

### 2. Create Virtual Environment

\`\`\`bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\\Scripts\\activate

# On macOS/Linux:
source venv/bin/activate
\`\`\`

### 3. Install Dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Set Up Environment Variables

\`\`\`bash
# Copy example env file
cp .env.example .env

# Edit .env file with your settings (optional for local development)
\`\`\`

### 5. Run the Application

\`\`\`bash
python app.py
\`\`\`

The application will be available at `http://localhost:5000`

## 📁 Project Structure

\`\`\`
ai-resume-screening-system/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── models.py                   # Database models
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
│
├── utils/                     # Utility modules
│   ├── pdf_parser.py         # Resume parsing logic
│   └── ml_matcher.py         # ML matching algorithms
│
├── templates/                 # HTML templates
│   └── index.html            # Main application page
│
├── static/                    # Static files
│   ├── css/
│   │   └── style.css         # Application styles
│   └── js/
│       └── app.js            # Frontend JavaScript
│
├── uploads/                   # Uploaded resume files
├── models/                    # ML model storage
└── README.md                  # This file
\`\`\`

## 🎯 How to Use

### 1. Upload Resume
1. Go to "Upload Resume" tab
2. Drag & drop or click to select a PDF/DOCX resume
3. System automatically extracts and analyzes the resume
4. View extracted information (name, email, skills, experience, education)

### 2. Create Job Description
1. Go to "Job Descriptions" tab
2. Fill in job details:
   - Job title
   - Description
   - Required skills (comma-separated)
   - Preferred skills (comma-separated)
   - Minimum experience
   - Education requirement
3. Click "Create Job Description"

### 3. Screen Resume
1. Go to "Screen Resume" tab
2. Select a resume from dropdown
3. Select a job description from dropdown
4. Click "Screen Resume"
5. View comprehensive results:
   - Overall match score
   - Individual component scores
   - Matched skills
   - Missing skills
   - Skill gap analysis
   - Recommendation

### 4. View Results
- Go to "Results" tab to see all screening history
- Each result shows scores and recommendations

### 5. Analytics
- Go to "Analytics" tab for system-wide statistics
- View total resumes, jobs, screenings, and average scores

## 🧠 Machine Learning Explanation

### TF-IDF (Term Frequency-Inverse Document Frequency)

The system uses TF-IDF vectorization to convert text into numerical features:

1. **Term Frequency (TF)**: How often a word appears in a document
2. **Inverse Document Frequency (IDF)**: How unique/important a word is across documents
3. **TF-IDF Score**: TF × IDF - gives higher weight to important, relevant terms

### Cosine Similarity

Measures similarity between resume and job description vectors:

\`\`\`
similarity = (A · B) / (||A|| × ||B||)
\`\`\`

- Range: 0 to 1 (0% to 100%)
- Higher score = better match

### Scoring Algorithm

\`\`\`python
Overall Score = (
    Skill Match × 0.40 +      # 40% weight
    Text Similarity × 0.25 +   # 25% weight
    Experience × 0.20 +        # 20% weight
    Education × 0.15           # 15% weight
)
\`\`\`

### Skill Matching

- **Required Skills**: 70% weight in skill score
- **Preferred Skills**: 30% weight in skill score
- Exact and partial matching supported
- Case-insensitive matching

## 📊 API Endpoints

### Resumes
- `POST /api/upload-resume` - Upload and parse resume
- `GET /api/resumes` - Get all resumes
- `GET /api/resumes/<id>` - Get specific resume
- `DELETE /api/resumes/<id>` - Delete resume

### Job Descriptions
- `POST /api/jobs` - Create job description
- `GET /api/jobs` - Get all jobs
- `GET /api/jobs/<id>` - Get specific job
- `DELETE /api/jobs/<id>` - Delete job

### Screening
- `POST /api/screen` - Screen resume against job
- `GET /api/screenings` - Get all screening results
- `GET /api/screenings/<id>` - Get specific screening

### Analytics
- `GET /api/analytics` - Get system analytics

## 🔧 Configuration

Edit `config.py` or `.env` file to customize:

\`\`\`python
# Database
DATABASE_URL = 'sqlite:///resume_screening.db'

# Upload settings
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# Add custom skills to COMMON_SKILLS list
\`\`\`

## 🎨 Customization

### Adding New Skills

Edit `config.py` and add skills to `COMMON_SKILLS` list:

\`\`\`python
COMMON_SKILLS = [
    'python', 'java', 'javascript',
    # Add your skills here
    'your-skill-1', 'your-skill-2'
]
\`\`\`

### Adjusting Scoring Weights

Edit `utils/ml_matcher.py` in the `screen_resume` method:

\`\`\`python
overall_score = (
    skill_match['overall_score'] * 0.40 +  # Adjust weight
    text_similarity * 0.25 +                # Adjust weight
    experience_score * 0.20 +               # Adjust weight
    education_score * 0.15                  # Adjust weight
)
\`\`\`

## 🐛 Troubleshooting

### PDF Extraction Issues

If PDF text extraction fails:
1. Ensure PDF is not scanned/image-based
2. Try converting to DOCX format
3. Check if PDF has copy protection

### Database Errors

\`\`\`bash
# Reset database
rm resume_screening.db
python app.py  # Will recreate database
\`\`\`

### Module Import Errors

\`\`\`bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
\`\`\`

## 📈 Future Enhancements

- [ ] Support for more file formats (TXT, RTF)
- [ ] Advanced NLP with spaCy/NLTK
- [ ] Deep learning models (BERT, GPT)
- [ ] Batch resume processing
- [ ] Email integration
- [ ] ATS (Applicant Tracking System) integration
- [ ] Multi-language support
- [ ] Resume ranking and sorting
- [ ] Interview scheduling
- [ ] Candidate communication

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Rahul Mishra**
- GitHub: [@rahul700raj](https://github.com/rahul700raj)
- Email: rm2778643@gmail.com

## 🙏 Acknowledgments

- scikit-learn for ML algorithms
- Flask for the web framework
- PyPDF2 and pdfplumber for PDF parsing
- All contributors and users

## 📞 Support

If you have any questions or need help, please:
- Open an issue on GitHub
- Contact: rm2778643@gmail.com

---

Made with ❤️ by Rahul Mishra
