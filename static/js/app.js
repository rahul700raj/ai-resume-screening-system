// API Base URL
const API_URL = '/api';

// Tab Management
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(`${tabName}-tab`).classList.add('active');
    event.target.classList.add('active');
    
    // Load data for specific tabs
    if (tabName === 'upload') {
        loadResumes();
    } else if (tabName === 'jobs') {
        loadJobs();
    } else if (tabName === 'screen') {
        loadScreeningOptions();
    } else if (tabName === 'results') {
        loadScreenings();
    } else if (tabName === 'analytics') {
        loadAnalytics();
    }
}

// Resume Upload
const uploadArea = document.getElementById('upload-area');
const resumeFile = document.getElementById('resume-file');

uploadArea.addEventListener('click', () => resumeFile.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        resumeFile.files = files;
        uploadResume(files[0]);
    }
});

resumeFile.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        uploadResume(e.target.files[0]);
    }
});

async function uploadResume(file) {
    const statusDiv = document.getElementById('upload-status');
    statusDiv.style.display = 'block';
    statusDiv.className = 'status-message status-loading';
    statusDiv.innerHTML = '<div class="loading"></div> Uploading and analyzing resume...';
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch(`${API_URL}/upload-resume`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            statusDiv.className = 'status-message status-success';
            statusDiv.textContent = '✓ Resume uploaded and analyzed successfully!';
            
            displayResumePreview(data.resume);
            loadResumes();
            
            // Clear file input
            resumeFile.value = '';
        } else {
            throw new Error(data.error || 'Upload failed');
        }
    } catch (error) {
        statusDiv.className = 'status-message status-error';
        statusDiv.textContent = `✗ Error: ${error.message}`;
    }
}

function displayResumePreview(resume) {
    const previewDiv = document.getElementById('resume-preview');
    const detailsDiv = document.getElementById('resume-details');
    
    previewDiv.style.display = 'block';
    
    detailsDiv.innerHTML = `
        <div class="info-grid">
            <div class="info-item">
                <strong>Candidate Name</strong>
                <span>${resume.candidate_name || 'Not detected'}</span>
            </div>
            <div class="info-item">
                <strong>Email</strong>
                <span>${resume.candidate_email || 'Not detected'}</span>
            </div>
            <div class="info-item">
                <strong>Phone</strong>
                <span>${resume.candidate_phone || 'Not detected'}</span>
            </div>
            <div class="info-item">
                <strong>Experience</strong>
                <span>${resume.experience_years || 0} years</span>
            </div>
            <div class="info-item">
                <strong>Education</strong>
                <span>${resume.education_level || 'Not specified'}</span>
            </div>
            <div class="info-item">
                <strong>Skills Found</strong>
                <span>${resume.skills_found.length} skills</span>
            </div>
        </div>
        <div style="margin-top: 16px;">
            <strong>Skills:</strong>
            <div class="skills-container">
                ${resume.skills_found.map(skill => `<span class="skill-tag">${skill}</span>`).join('')}
            </div>
        </div>
    `;
}

async function loadResumes() {
    try {
        const response = await fetch(`${API_URL}/resumes`);
        const data = await response.json();
        
        const listDiv = document.getElementById('resumes-list');
        
        if (data.resumes.length === 0) {
            listDiv.innerHTML = '<div class="empty-state"><div class="empty-state-icon">📄</div><p>No resumes uploaded yet</p></div>';
            return;
        }
        
        listDiv.innerHTML = data.resumes.map(resume => `
            <div class="list-item">
                <div class="list-item-content">
                    <h4>${resume.candidate_name || resume.filename}</h4>
                    <p>📧 ${resume.candidate_email || 'N/A'} | 📞 ${resume.candidate_phone || 'N/A'}</p>
                    <p>💼 ${resume.experience_years || 0} years | 🎓 ${resume.education_level || 'N/A'} | 🔧 ${resume.skills_found.length} skills</p>
                </div>
                <div class="list-item-actions">
                    <button class="btn btn-danger btn-small" onclick="deleteResume(${resume.id})">Delete</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading resumes:', error);
    }
}

async function deleteResume(id) {
    if (!confirm('Are you sure you want to delete this resume?')) return;
    
    try {
        const response = await fetch(`${API_URL}/resumes/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadResumes();
        }
    } catch (error) {
        console.error('Error deleting resume:', error);
    }
}

// Job Description Management
document.getElementById('job-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const jobData = {
        title: document.getElementById('job-title').value,
        description: document.getElementById('job-description').value,
        min_experience: parseFloat(document.getElementById('job-experience').value) || 0,
        education_required: document.getElementById('job-education').value,
        required_skills: document.getElementById('job-required-skills').value
            .split(',').map(s => s.trim()).filter(s => s),
        preferred_skills: document.getElementById('job-preferred-skills').value
            .split(',').map(s => s.trim()).filter(s => s)
    };
    
    try {
        const response = await fetch(`${API_URL}/jobs`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(jobData)
        });
        
        if (response.ok) {
            alert('Job description created successfully!');
            e.target.reset();
            loadJobs();
        } else {
            const data = await response.json();
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
});

async function loadJobs() {
    try {
        const response = await fetch(`${API_URL}/jobs`);
        const data = await response.json();
        
        const listDiv = document.getElementById('jobs-list');
        
        if (data.jobs.length === 0) {
            listDiv.innerHTML = '<div class="empty-state"><div class="empty-state-icon">💼</div><p>No job descriptions created yet</p></div>';
            return;
        }
        
        listDiv.innerHTML = data.jobs.map(job => `
            <div class="list-item">
                <div class="list-item-content">
                    <h4>${job.title}</h4>
                    <p>💼 ${job.min_experience || 0} years experience | 🎓 ${job.education_required || 'N/A'}</p>
                    <p>Required: ${job.required_skills.length} skills | Preferred: ${job.preferred_skills.length} skills</p>
                </div>
                <div class="list-item-actions">
                    <button class="btn btn-danger btn-small" onclick="deleteJob(${job.id})">Delete</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading jobs:', error);
    }
}

async function deleteJob(id) {
    if (!confirm('Are you sure you want to delete this job description?')) return;
    
    try {
        const response = await fetch(`${API_URL}/jobs/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadJobs();
        }
    } catch (error) {
        console.error('Error deleting job:', error);
    }
}

// Screening
async function loadScreeningOptions() {
    try {
        const [resumesRes, jobsRes] = await Promise.all([
            fetch(`${API_URL}/resumes`),
            fetch(`${API_URL}/jobs`)
        ]);
        
        const resumesData = await resumesRes.json();
        const jobsData = await jobsRes.json();
        
        const resumeSelect = document.getElementById('screen-resume');
        const jobSelect = document.getElementById('screen-job');
        
        resumeSelect.innerHTML = '<option value="">-- Choose Resume --</option>' +
            resumesData.resumes.map(r => 
                `<option value="${r.id}">${r.candidate_name || r.filename}</option>`
            ).join('');
        
        jobSelect.innerHTML = '<option value="">-- Choose Job --</option>' +
            jobsData.jobs.map(j => 
                `<option value="${j.id}">${j.title}</option>`
            ).join('');
    } catch (error) {
        console.error('Error loading screening options:', error);
    }
}

document.getElementById('screen-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const resumeId = document.getElementById('screen-resume').value;
    const jobId = document.getElementById('screen-job').value;
    
    const resultDiv = document.getElementById('screening-result');
    resultDiv.style.display = 'block';
    resultDiv.innerHTML = '<div class="loading"></div> Analyzing resume...';
    
    try {
        const response = await fetch(`${API_URL}/screen`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ resume_id: resumeId, job_id: jobId })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayScreeningResult(data.screening, data.resume, data.job);
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        resultDiv.innerHTML = `<p style="color: #fee2e2;">Error: ${error.message}</p>`;
    }
});

function displayScreeningResult(screening, resume, job) {
    const resultDiv = document.getElementById('screening-result');
    
    const recommendationClass = {
        'Highly Recommended': 'success',
        'Recommended': 'success',
        'Maybe': 'warning',
        'Not Recommended': 'danger'
    }[screening.recommendation] || 'warning';
    
    resultDiv.innerHTML = `
        <div class="score-header">
            <h2>Screening Results</h2>
            <p>${resume.candidate_name || 'Candidate'} for ${job.title}</p>
            <div class="overall-score">${screening.overall_score.toFixed(1)}%</div>
            <div class="recommendation ${recommendationClass}">${screening.recommendation}</div>
        </div>
        
        <div class="scores-grid">
            <div class="score-card">
                <h4>Skill Match</h4>
                <div class="score">${screening.skill_match_score.toFixed(1)}%</div>
            </div>
            <div class="score-card">
                <h4>Text Similarity</h4>
                <div class="score">${screening.text_similarity_score.toFixed(1)}%</div>
            </div>
            <div class="score-card">
                <h4>Experience</h4>
                <div class="score">${screening.experience_score.toFixed(1)}%</div>
            </div>
            <div class="score-card">
                <h4>Education</h4>
                <div class="score">${screening.education_score.toFixed(1)}%</div>
            </div>
        </div>
        
        <div class="skills-section">
            <h3>✓ Matched Skills (${screening.matched_skills.length})</h3>
            <div class="skills-container">
                ${screening.matched_skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')}
            </div>
        </div>
        
        <div class="skills-section">
            <h3>✗ Missing Skills (${screening.missing_skills.length})</h3>
            <div class="skills-container">
                ${screening.missing_skills.map(skill => `<span class="skill-tag missing">${skill}</span>`).join('')}
            </div>
        </div>
        
        <div class="gap-analysis">
            <h3>Skill Gap Analysis</h3>
            <div class="gap-item">
                <h4>Required Skills</h4>
                <p>Matched: ${screening.skill_gap_analysis.required_matched.length} | 
                   Missing: ${screening.skill_gap_analysis.required_missing.length}</p>
            </div>
            <div class="gap-item">
                <h4>Preferred Skills</h4>
                <p>Matched: ${screening.skill_gap_analysis.preferred_matched.length} | 
                   Missing: ${screening.skill_gap_analysis.preferred_missing.length}</p>
            </div>
            <div class="gap-item">
                <h4>Notes</h4>
                <p>${screening.notes}</p>
            </div>
        </div>
    `;
}

async function loadScreenings() {
    try {
        const response = await fetch(`${API_URL}/screenings`);
        const data = await response.json();
        
        const listDiv = document.getElementById('screenings-list');
        
        if (data.screenings.length === 0) {
            listDiv.innerHTML = '<div class="empty-state"><div class="empty-state-icon">📊</div><p>No screening results yet</p></div>';
            return;
        }
        
        listDiv.innerHTML = data.screenings.map(s => `
            <div class="list-item">
                <div class="list-item-content">
                    <h4>${s.resume.candidate_name || 'Candidate'} → ${s.job.title}</h4>
                    <p>Overall Score: ${s.overall_score.toFixed(1)}% | ${s.recommendation}</p>
                    <p>Skills: ${s.skill_match_score.toFixed(1)}% | Experience: ${s.experience_score.toFixed(1)}% | Education: ${s.education_score.toFixed(1)}%</p>
                    <p style="font-size: 12px; color: #6b7280;">Screened: ${new Date(s.screened_at).toLocaleString()}</p>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading screenings:', error);
    }
}

async function loadAnalytics() {
    try {
        const response = await fetch(`${API_URL}/analytics`);
        const data = await response.json();
        
        const analyticsDiv = document.getElementById('analytics-content');
        
        analyticsDiv.innerHTML = `
            <div class="analytics-card">
                <h3>Total Resumes</h3>
                <div class="value">${data.total_resumes}</div>
                <div class="label">Uploaded</div>
            </div>
            <div class="analytics-card">
                <h3>Job Descriptions</h3>
                <div class="value">${data.total_jobs}</div>
                <div class="label">Created</div>
            </div>
            <div class="analytics-card">
                <h3>Screenings</h3>
                <div class="value">${data.total_screenings}</div>
                <div class="label">Completed</div>
            </div>
            <div class="analytics-card">
                <h3>Avg Overall Score</h3>
                <div class="value">${data.average_overall_score.toFixed(1)}%</div>
                <div class="label">Performance</div>
            </div>
            <div class="analytics-card">
                <h3>Avg Skill Match</h3>
                <div class="value">${data.average_skill_score.toFixed(1)}%</div>
                <div class="label">Skills</div>
            </div>
        `;
    } catch (error) {
        console.error('Error loading analytics:', error);
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadResumes();
});
