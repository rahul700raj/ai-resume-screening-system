# API Documentation

Complete API reference for the AI Resume Screening System.

## Base URL

\`\`\`
http://localhost:5000/api
\`\`\`

## Response Format

All API responses follow this format:

### Success Response
\`\`\`json
{
  "message": "Success message",
  "data": { ... }
}
\`\`\`

### Error Response
\`\`\`json
{
  "error": "Error message"
}
\`\`\`

---

## Endpoints

### Health Check

Check if the API is running.

**Endpoint:** `GET /api/health`

**Response:**
\`\`\`json
{
  "status": "ok",
  "message": "AI Resume Screening System is running",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
\`\`\`

---

## Resume Management

### Upload Resume

Upload and parse a resume file (PDF or DOCX).

**Endpoint:** `POST /api/upload-resume`

**Content-Type:** `multipart/form-data`

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| file | File | Yes | Resume file (PDF or DOCX, max 16MB) |

**Example Request:**
\`\`\`bash
curl -X POST http://localhost:5000/api/upload-resume \
  -F "file=@resume.pdf"
\`\`\`

**Response:**
\`\`\`json
{
  "message": "Resume uploaded and parsed successfully",
  "resume": {
    "id": 1,
    "filename": "john_doe_resume.pdf",
    "candidate_name": "John Doe",
    "candidate_email": "john.doe@email.com",
    "candidate_phone": "+1-234-567-8900",
    "skills_found": ["Python", "Flask", "SQL", "Machine Learning"],
    "experience_years": 5.0,
    "education_level": "Bachelors",
    "uploaded_at": "2024-01-15T10:30:00.000Z"
  }
}
\`\`\`

### Get All Resumes

Retrieve all uploaded resumes.

**Endpoint:** `GET /api/resumes`

**Response:**
\`\`\`json
{
  "resumes": [
    {
      "id": 1,
      "filename": "john_doe_resume.pdf",
      "candidate_name": "John Doe",
      "candidate_email": "john.doe@email.com",
      "candidate_phone": "+1-234-567-8900",
      "skills_found": ["Python", "Flask", "SQL"],
      "experience_years": 5.0,
      "education_level": "Bachelors",
      "uploaded_at": "2024-01-15T10:30:00.000Z"
    }
  ],
  "total": 1
}
\`\`\`

### Get Specific Resume

Retrieve a specific resume by ID.

**Endpoint:** `GET /api/resumes/<resume_id>`

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| resume_id | Integer | Yes | Resume ID |

**Response:**
\`\`\`json
{
  "resume": {
    "id": 1,
    "filename": "john_doe_resume.pdf",
    "candidate_name": "John Doe",
    "candidate_email": "john.doe@email.com",
    "candidate_phone": "+1-234-567-8900",
    "skills_found": ["Python", "Flask", "SQL"],
    "experience_years": 5.0,
    "education_level": "Bachelors",
    "uploaded_at": "2024-01-15T10:30:00.000Z"
  }
}
\`\`\`

### Delete Resume

Delete a resume and its associated file.

**Endpoint:** `DELETE /api/resumes/<resume_id>`

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| resume_id | Integer | Yes | Resume ID |

**Response:**
\`\`\`json
{
  "message": "Resume deleted successfully"
}
\`\`\`

---

## Job Description Management

### Create Job Description

Create a new job description.

**Endpoint:** `POST /api/jobs`

**Content-Type:** `application/json`

**Request Body:**
\`\`\`json
{
  "title": "Senior Python Developer",
  "description": "We are looking for an experienced Python developer...",
  "required_skills": ["Python", "Django", "PostgreSQL"],
  "preferred_skills": ["Docker", "AWS", "React"],
  "min_experience": 3.0,
  "education_required": "Bachelors"
}
\`\`\`

**Response:**
\`\`\`json
{
  "message": "Job description created successfully",
  "job": {
    "id": 1,
    "title": "Senior Python Developer",
    "description": "We are looking for an experienced Python developer...",
    "required_skills": ["Python", "Django", "PostgreSQL"],
    "preferred_skills": ["Docker", "AWS", "React"],
    "min_experience": 3.0,
    "education_required": "Bachelors",
    "created_at": "2024-01-15T10:30:00.000Z"
  }
}
\`\`\`

### Get All Jobs

Retrieve all job descriptions.

**Endpoint:** `GET /api/jobs`

**Response:**
\`\`\`json
{
  "jobs": [
    {
      "id": 1,
      "title": "Senior Python Developer",
      "description": "We are looking for...",
      "required_skills": ["Python", "Django", "PostgreSQL"],
      "preferred_skills": ["Docker", "AWS"],
      "min_experience": 3.0,
      "education_required": "Bachelors",
      "created_at": "2024-01-15T10:30:00.000Z"
    }
  ],
  "total": 1
}
\`\`\`

### Get Specific Job

Retrieve a specific job description by ID.

**Endpoint:** `GET /api/jobs/<job_id>`

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| job_id | Integer | Yes | Job ID |

**Response:**
\`\`\`json
{
  "job": {
    "id": 1,
    "title": "Senior Python Developer",
    "description": "We are looking for...",
    "required_skills": ["Python", "Django", "PostgreSQL"],
    "preferred_skills": ["Docker", "AWS"],
    "min_experience": 3.0,
    "education_required": "Bachelors",
    "created_at": "2024-01-15T10:30:00.000Z"
  }
}
\`\`\`

### Delete Job

Delete a job description.

**Endpoint:** `DELETE /api/jobs/<job_id>`

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| job_id | Integer | Yes | Job ID |

**Response:**
\`\`\`json
{
  "message": "Job description deleted successfully"
}
\`\`\`

---

## Resume Screening

### Screen Resume

Screen a resume against a job description using AI.

**Endpoint:** `POST /api/screen`

**Content-Type:** `application/json`

**Request Body:**
\`\`\`json
{
  "resume_id": 1,
  "job_id": 1
}
\`\`\`

**Response:**
\`\`\`json
{
  "message": "Resume screened successfully",
  "screening": {
    "id": 1,
    "resume_id": 1,
    "job_id": 1,
    "overall_score": 75.5,
    "skill_match_score": 66.7,
    "text_similarity_score": 82.3,
    "experience_score": 100.0,
    "education_score": 100.0,
    "matched_skills": ["Python", "SQL"],
    "missing_skills": ["Django", "PostgreSQL", "Docker", "AWS"],
    "skill_gap_analysis": {
      "required_matched": ["Python"],
      "required_missing": ["Django", "PostgreSQL"],
      "preferred_matched": [],
      "preferred_missing": ["Docker", "AWS"],
      "total_matched": 1,
      "total_missing": 4
    },
    "recommendation": "Recommended",
    "notes": "• Moderate skill match, some training may be needed | ✓ Meets or exceeds experience requirements | ✓ Meets education requirements",
    "screened_at": "2024-01-15T10:30:00.000Z"
  },
  "resume": {
    "id": 1,
    "filename": "john_doe_resume.pdf",
    "candidate_name": "John Doe"
  },
  "job": {
    "id": 1,
    "title": "Senior Python Developer"
  }
}
\`\`\`

### Get All Screenings

Retrieve all screening results.

**Endpoint:** `GET /api/screenings`

**Response:**
\`\`\`json
{
  "screenings": [
    {
      "id": 1,
      "resume_id": 1,
      "job_id": 1,
      "overall_score": 75.5,
      "skill_match_score": 66.7,
      "text_similarity_score": 82.3,
      "experience_score": 100.0,
      "education_score": 100.0,
      "matched_skills": ["Python", "SQL"],
      "missing_skills": ["Django", "PostgreSQL"],
      "recommendation": "Recommended",
      "screened_at": "2024-01-15T10:30:00.000Z",
      "resume": {
        "id": 1,
        "candidate_name": "John Doe"
      },
      "job": {
        "id": 1,
        "title": "Senior Python Developer"
      }
    }
  ],
  "total": 1
}
\`\`\`

### Get Specific Screening

Retrieve a specific screening result by ID.

**Endpoint:** `GET /api/screenings/<screening_id>`

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| screening_id | Integer | Yes | Screening ID |

**Response:**
\`\`\`json
{
  "screening": {
    "id": 1,
    "overall_score": 75.5,
    "skill_match_score": 66.7,
    "recommendation": "Recommended",
    "resume": { ... },
    "job": { ... }
  }
}
\`\`\`

---

## Analytics

### Get System Analytics

Retrieve system-wide analytics and statistics.

**Endpoint:** `GET /api/analytics`

**Response:**
\`\`\`json
{
  "total_resumes": 25,
  "total_jobs": 10,
  "total_screenings": 50,
  "average_overall_score": 68.5,
  "average_skill_score": 62.3,
  "recommendations": {
    "Highly Recommended": 10,
    "Recommended": 20,
    "Maybe": 15,
    "Not Recommended": 5
  }
}
\`\`\`

---

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Invalid input |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error |

---

## Rate Limiting

Currently, there are no rate limits. For production use, consider implementing rate limiting.

---

## Authentication

Currently, the API doesn't require authentication. For production use, implement JWT or OAuth2 authentication.

---

## Examples

### Python Example

\`\`\`python
import requests

# Upload resume
with open('resume.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:5000/api/upload-resume',
        files={'file': f}
    )
    resume_data = response.json()

# Create job
job_data = {
    'title': 'Python Developer',
    'description': 'Looking for Python developer...',
    'required_skills': ['Python', 'Flask'],
    'min_experience': 2
}
response = requests.post(
    'http://localhost:5000/api/jobs',
    json=job_data
)
job = response.json()

# Screen resume
screen_data = {
    'resume_id': resume_data['resume']['id'],
    'job_id': job['job']['id']
}
response = requests.post(
    'http://localhost:5000/api/screen',
    json=screen_data
)
result = response.json()
print(f"Overall Score: {result['screening']['overall_score']}%")
\`\`\`

### JavaScript Example

\`\`\`javascript
// Upload resume
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const resumeResponse = await fetch('/api/upload-resume', {
  method: 'POST',
  body: formData
});
const resumeData = await resumeResponse.json();

// Create job
const jobResponse = await fetch('/api/jobs', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    title: 'Python Developer',
    description: 'Looking for...',
    required_skills: ['Python', 'Flask'],
    min_experience: 2
  })
});
const jobData = await jobResponse.json();

// Screen resume
const screenResponse = await fetch('/api/screen', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    resume_id: resumeData.resume.id,
    job_id: jobData.job.id
  })
});
const result = await screenResponse.json();
console.log(`Score: ${result.screening.overall_score}%`);
\`\`\`

---

## Postman Collection

Import this collection into Postman for easy API testing:

\`\`\`json
{
  "info": {
    "name": "AI Resume Screening API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Upload Resume",
      "request": {
        "method": "POST",
        "url": "{{base_url}}/api/upload-resume",
        "body": {
          "mode": "formdata",
          "formdata": [
            {
              "key": "file",
              "type": "file",
              "src": ""
            }
          ]
        }
      }
    },
    {
      "name": "Create Job",
      "request": {
        "method": "POST",
        "url": "{{base_url}}/api/jobs",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"title\": \"Python Developer\",\n  \"description\": \"Looking for...\",\n  \"required_skills\": [\"Python\", \"Flask\"],\n  \"min_experience\": 2\n}"
        }
      }
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:5000"
    }
  ]
}
\`\`\`

---

For more information, see the [README](README.md) or [ML Explanation](ML_EXPLANATION.md).
