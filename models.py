from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Resume(db.Model):
    """Resume model for storing uploaded resumes"""
    
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    extracted_text = db.Column(db.Text)
    
    # Candidate information
    candidate_name = db.Column(db.String(200))
    candidate_email = db.Column(db.String(200))
    candidate_phone = db.Column(db.String(50))
    
    # Analysis results
    skills_found = db.Column(db.Text)  # JSON string
    experience_years = db.Column(db.Float)
    education_level = db.Column(db.String(100))
    
    # Timestamps
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    screenings = db.relationship('Screening', backref='resume', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.original_filename,
            'candidate_name': self.candidate_name,
            'candidate_email': self.candidate_email,
            'candidate_phone': self.candidate_phone,
            'skills_found': json.loads(self.skills_found) if self.skills_found else [],
            'experience_years': self.experience_years,
            'education_level': self.education_level,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }


class JobDescription(db.Model):
    """Job description model"""
    
    __tablename__ = 'job_descriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    required_skills = db.Column(db.Text)  # JSON string
    preferred_skills = db.Column(db.Text)  # JSON string
    min_experience = db.Column(db.Float)
    education_required = db.Column(db.String(100))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    screenings = db.relationship('Screening', backref='job', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'required_skills': json.loads(self.required_skills) if self.required_skills else [],
            'preferred_skills': json.loads(self.preferred_skills) if self.preferred_skills else [],
            'min_experience': self.min_experience,
            'education_required': self.education_required,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Screening(db.Model):
    """Screening results model"""
    
    __tablename__ = 'screenings'
    
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job_descriptions.id'), nullable=False)
    
    # Scoring
    overall_score = db.Column(db.Float)
    skill_match_score = db.Column(db.Float)
    experience_score = db.Column(db.Float)
    education_score = db.Column(db.Float)
    text_similarity_score = db.Column(db.Float)
    
    # Analysis
    matched_skills = db.Column(db.Text)  # JSON string
    missing_skills = db.Column(db.Text)  # JSON string
    skill_gap_analysis = db.Column(db.Text)  # JSON string
    
    # Recommendation
    recommendation = db.Column(db.String(50))  # 'Highly Recommended', 'Recommended', 'Maybe', 'Not Recommended'
    notes = db.Column(db.Text)
    
    # Timestamp
    screened_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'resume_id': self.resume_id,
            'job_id': self.job_id,
            'overall_score': round(self.overall_score, 2) if self.overall_score else 0,
            'skill_match_score': round(self.skill_match_score, 2) if self.skill_match_score else 0,
            'experience_score': round(self.experience_score, 2) if self.experience_score else 0,
            'education_score': round(self.education_score, 2) if self.education_score else 0,
            'text_similarity_score': round(self.text_similarity_score, 2) if self.text_similarity_score else 0,
            'matched_skills': json.loads(self.matched_skills) if self.matched_skills else [],
            'missing_skills': json.loads(self.missing_skills) if self.missing_skills else [],
            'skill_gap_analysis': json.loads(self.skill_gap_analysis) if self.skill_gap_analysis else {},
            'recommendation': self.recommendation,
            'notes': self.notes,
            'screened_at': self.screened_at.isoformat() if self.screened_at else None
        }
