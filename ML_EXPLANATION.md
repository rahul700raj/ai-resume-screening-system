# Machine Learning Model Explanation

This document explains the machine learning algorithms and techniques used in the AI Resume Screening System.

## Overview

The system uses **Natural Language Processing (NLP)** and **Machine Learning** techniques to analyze and match resumes with job descriptions. The core algorithm is based on **TF-IDF vectorization** and **Cosine Similarity**.

## 1. TF-IDF (Term Frequency-Inverse Document Frequency)

### What is TF-IDF?

TF-IDF is a numerical statistic that reflects how important a word is to a document in a collection of documents.

### Components

#### Term Frequency (TF)
Measures how frequently a term appears in a document.

\`\`\`
TF(t, d) = (Number of times term t appears in document d) / (Total number of terms in document d)
\`\`\`

**Example:**
- Document: "Python developer with Python skills"
- TF("Python") = 2/5 = 0.4

#### Inverse Document Frequency (IDF)
Measures how important a term is across all documents.

\`\`\`
IDF(t) = log(Total number of documents / Number of documents containing term t)
\`\`\`

**Example:**
- Total documents: 100
- Documents with "Python": 20
- IDF("Python") = log(100/20) = 0.699

#### TF-IDF Score
\`\`\`
TF-IDF(t, d) = TF(t, d) × IDF(t)
\`\`\`

### Why TF-IDF?

1. **Highlights Important Terms**: Common words (the, is, and) get low scores
2. **Domain-Specific Terms**: Technical terms get higher scores
3. **Balanced Representation**: Considers both frequency and uniqueness

### Implementation

\`\`\`python
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(
    max_features=1000,      # Top 1000 features
    stop_words='english',   # Remove common words
    ngram_range=(1, 2),     # Unigrams and bigrams
    min_df=1                # Minimum document frequency
)

# Transform text to TF-IDF vectors
tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
\`\`\`

## 2. Cosine Similarity

### What is Cosine Similarity?

Cosine similarity measures the cosine of the angle between two vectors in a multi-dimensional space. It determines how similar two documents are, regardless of their size.

### Formula

\`\`\`
cosine_similarity(A, B) = (A · B) / (||A|| × ||B||)

Where:
- A · B = dot product of vectors A and B
- ||A|| = magnitude (length) of vector A
- ||B|| = magnitude (length) of vector B
\`\`\`

### Range

- **1.0**: Identical documents (0° angle)
- **0.0**: Completely different documents (90° angle)
- **-1.0**: Opposite documents (180° angle)

For our use case, we convert to percentage: `similarity × 100`

### Visual Example

\`\`\`
Resume Vector:     [0.5, 0.3, 0.8, 0.1]
Job Desc Vector:   [0.4, 0.4, 0.7, 0.2]

Cosine Similarity = 0.95 (95% match)
\`\`\`

### Implementation

\`\`\`python
from sklearn.metrics.pairwise import cosine_similarity

# Calculate similarity
similarity = cosine_similarity(
    tfidf_matrix[0:1],  # Resume vector
    tfidf_matrix[1:2]   # Job description vector
)[0][0]

# Convert to percentage
similarity_percentage = similarity * 100
\`\`\`

## 3. Skill Matching Algorithm

### Exact Matching

The system performs case-insensitive exact matching of skills:

\`\`\`python
resume_skills = ['Python', 'Flask', 'SQL']
required_skills = ['python', 'django', 'postgresql']

# Normalize to lowercase
resume_skills_lower = [s.lower() for s in resume_skills]
required_skills_lower = [s.lower() for s in required_skills]

# Find matches
matched = [skill for skill in required_skills 
           if skill.lower() in resume_skills_lower]
# Result: ['python']

missing = [skill for skill in required_skills 
           if skill.lower() not in resume_skills_lower]
# Result: ['django', 'postgresql']
\`\`\`

### Skill Score Calculation

\`\`\`python
# Required skills: 70% weight
required_score = (matched_required / total_required) × 100 × 0.7

# Preferred skills: 30% weight
preferred_score = (matched_preferred / total_preferred) × 100 × 0.3

# Overall skill score
skill_score = required_score + preferred_score
\`\`\`

## 4. Experience Scoring

### Algorithm

\`\`\`python
def calculate_experience_score(candidate_years, required_years):
    if required_years == 0:
        return 100.0
    
    if candidate_years >= required_years:
        # Bonus for extra experience (up to 20%)
        bonus = min((candidate_years - required_years) / required_years × 20, 20)
        return min(100.0 + bonus, 120.0)
    else:
        # Penalty for less experience
        return (candidate_years / required_years) × 100
\`\`\`

### Examples

| Candidate | Required | Score | Explanation |
|-----------|----------|-------|-------------|
| 5 years   | 3 years  | 113%  | 100% + 13% bonus |
| 3 years   | 3 years  | 100%  | Exact match |
| 2 years   | 3 years  | 67%   | 2/3 = 66.7% |
| 0 years   | 0 years  | 100%  | No requirement |

## 5. Education Scoring

### Hierarchy

\`\`\`python
education_hierarchy = {
    'high school': 1,
    'diploma': 2,
    'bachelors': 3,
    'masters': 4,
    'phd': 5
}
\`\`\`

### Scoring Logic

| Candidate Level | Required Level | Score | Explanation |
|----------------|----------------|-------|-------------|
| Masters        | Bachelors      | 100%  | Exceeds requirement |
| Bachelors      | Bachelors      | 100%  | Exact match |
| Bachelors      | Masters        | 75%   | One level below |
| Diploma        | Masters        | 50%   | Two levels below |
| High School    | Masters        | 25%   | More than two levels below |

## 6. Overall Score Calculation

### Weighted Average

\`\`\`python
overall_score = (
    skill_match_score × 0.40 +      # 40% weight
    text_similarity_score × 0.25 +   # 25% weight
    experience_score × 0.20 +        # 20% weight
    education_score × 0.15           # 15% weight
)

# Cap at 100%
overall_score = min(overall_score, 100)
\`\`\`

### Weight Rationale

1. **Skills (40%)**: Most important - directly indicates capability
2. **Text Similarity (25%)**: Shows overall alignment with job description
3. **Experience (20%)**: Important but can be compensated with skills
4. **Education (15%)**: Least weight - skills matter more than degrees

## 7. Recommendation Generation

### Thresholds

\`\`\`python
if overall_score >= 80:
    recommendation = "Highly Recommended"
elif overall_score >= 65:
    recommendation = "Recommended"
elif overall_score >= 50:
    recommendation = "Maybe"
else:
    recommendation = "Not Recommended"
\`\`\`

### Distribution

| Score Range | Recommendation | Meaning |
|-------------|----------------|---------|
| 80-100%     | Highly Recommended | Excellent match, proceed to interview |
| 65-79%      | Recommended | Good match, worth considering |
| 50-64%      | Maybe | Moderate match, review carefully |
| 0-49%       | Not Recommended | Poor match, likely not suitable |

## 8. Model Training (Future Enhancement)

Currently, the system uses **unsupervised learning** (TF-IDF + Cosine Similarity). Future versions could include:

### Supervised Learning

\`\`\`python
from sklearn.ensemble import RandomForestClassifier

# Features
X = [
    [skill_score, text_sim, exp_score, edu_score],
    # ... more samples
]

# Labels (historical hiring decisions)
y = [1, 0, 1, 1, 0]  # 1 = hired, 0 = not hired

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Predict
prediction = model.predict([[75, 80, 90, 100]])
\`\`\`

### Deep Learning

\`\`\`python
from transformers import BertModel

# Use BERT for semantic understanding
model = BertModel.from_pretrained('bert-base-uncased')

# Get embeddings
resume_embedding = model(resume_tokens)
job_embedding = model(job_tokens)

# Calculate similarity
similarity = cosine_similarity(resume_embedding, job_embedding)
\`\`\`

## 9. Performance Metrics

### Accuracy Measures

1. **Precision**: Of all recommended candidates, how many were actually good?
2. **Recall**: Of all good candidates, how many did we recommend?
3. **F1-Score**: Harmonic mean of precision and recall

\`\`\`python
from sklearn.metrics import precision_score, recall_score, f1_score

precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)
\`\`\`

## 10. Advantages & Limitations

### Advantages

✅ **Fast**: Processes resumes in seconds  
✅ **Objective**: Removes human bias  
✅ **Scalable**: Can handle thousands of resumes  
✅ **Consistent**: Same criteria for all candidates  
✅ **Explainable**: Clear scoring breakdown  

### Limitations

❌ **Context Understanding**: May miss nuanced experience  
❌ **Format Dependent**: Works best with well-formatted resumes  
❌ **Keyword Focused**: May miss synonyms or related skills  
❌ **No Soft Skills**: Doesn't evaluate personality or culture fit  
❌ **Static Skills List**: Requires manual updates for new technologies  

## 11. Best Practices

### For Best Results

1. **Use Clear Job Descriptions**: Be specific about requirements
2. **List All Skills**: Include both required and preferred skills
3. **Standardize Formats**: Encourage standard resume formats
4. **Regular Updates**: Keep skill list current
5. **Human Review**: Use as a screening tool, not final decision

### Improving Accuracy

1. **Expand Skill Database**: Add more domain-specific skills
2. **Use Synonyms**: Map related skills (e.g., "JS" → "JavaScript")
3. **Weight Adjustment**: Tune weights based on your hiring data
4. **Threshold Tuning**: Adjust recommendation thresholds
5. **Feedback Loop**: Learn from hiring outcomes

## 12. Example Walkthrough

### Input

**Resume:**
- Skills: Python, Flask, SQL, Git
- Experience: 3 years
- Education: Bachelors

**Job Description:**
- Required Skills: Python, Django, PostgreSQL
- Preferred Skills: Docker, AWS
- Min Experience: 2 years
- Education: Bachelors

### Calculation

**Skill Match:**
- Required matched: 1/3 (Python) = 33.3%
- Preferred matched: 0/2 = 0%
- Skill score: (33.3 × 0.7) + (0 × 0.3) = 23.3%

**Text Similarity:**
- TF-IDF vectors calculated
- Cosine similarity: 65%

**Experience:**
- 3 years vs 2 required
- Score: 100% + 10% bonus = 110% → capped at 100%

**Education:**
- Bachelors vs Bachelors
- Score: 100%

**Overall:**
\`\`\`
(23.3 × 0.40) + (65 × 0.25) + (100 × 0.20) + (100 × 0.15)
= 9.32 + 16.25 + 20 + 15
= 60.57%
\`\`\`

**Recommendation:** Maybe

---

This explanation provides a comprehensive understanding of the ML algorithms used in the resume screening system. For questions or improvements, please open an issue on GitHub.
