import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Tuple
import json

class ResumeJobMatcher:
    """Machine Learning based resume and job description matcher"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1
        )
    
    def calculate_text_similarity(self, resume_text: str, job_description: str) -> float:
        """Calculate cosine similarity between resume and job description"""
        try:
            # Create TF-IDF vectors
            tfidf_matrix = self.vectorizer.fit_transform([resume_text, job_description])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity * 100)  # Convert to percentage
        except Exception as e:
            print(f"Error calculating similarity: {e}")
            return 0.0
    
    def calculate_skill_match(self, resume_skills: List[str], 
                            required_skills: List[str], 
                            preferred_skills: List[str] = None) -> Dict:
        """Calculate skill match score and identify gaps"""
        resume_skills_lower = [skill.lower() for skill in resume_skills]
        required_skills_lower = [skill.lower() for skill in required_skills]
        preferred_skills_lower = [skill.lower() for skill in (preferred_skills or [])]
        
        # Find matched and missing skills
        matched_required = [skill for skill in required_skills 
                          if skill.lower() in resume_skills_lower]
        missing_required = [skill for skill in required_skills 
                          if skill.lower() not in resume_skills_lower]
        
        matched_preferred = [skill for skill in (preferred_skills or []) 
                           if skill.lower() in resume_skills_lower]
        missing_preferred = [skill for skill in (preferred_skills or []) 
                           if skill.lower() not in resume_skills_lower]
        
        # Calculate scores
        required_score = (len(matched_required) / len(required_skills) * 100) if required_skills else 0
        preferred_score = (len(matched_preferred) / len(preferred_skills) * 100) if preferred_skills else 0
        
        # Overall skill score (70% required, 30% preferred)
        overall_skill_score = (required_score * 0.7) + (preferred_score * 0.3)
        
        return {
            'overall_score': overall_skill_score,
            'required_score': required_score,
            'preferred_score': preferred_score,
            'matched_required': matched_required,
            'missing_required': missing_required,
            'matched_preferred': matched_preferred,
            'missing_preferred': missing_preferred,
            'total_matched': len(matched_required) + len(matched_preferred),
            'total_missing': len(missing_required) + len(missing_preferred)
        }
    
    def calculate_experience_score(self, candidate_years: float, 
                                   required_years: float) -> float:
        """Calculate experience match score"""
        if required_years == 0:
            return 100.0
        
        if candidate_years >= required_years:
            # Bonus for extra experience (up to 20% bonus)
            bonus = min((candidate_years - required_years) / required_years * 20, 20)
            return min(100.0 + bonus, 120.0)
        else:
            # Penalty for less experience
            return (candidate_years / required_years) * 100
    
    def calculate_education_score(self, candidate_education: str, 
                                  required_education: str) -> float:
        """Calculate education match score"""
        education_hierarchy = {
            'high school': 1,
            'diploma': 2,
            'bachelors': 3,
            'masters': 4,
            'phd': 5
        }
        
        candidate_level = education_hierarchy.get(candidate_education.lower(), 0)
        required_level = education_hierarchy.get(required_education.lower(), 0)
        
        if required_level == 0:
            return 100.0  # No requirement specified
        
        if candidate_level >= required_level:
            return 100.0
        elif candidate_level == required_level - 1:
            return 75.0  # One level below
        elif candidate_level == required_level - 2:
            return 50.0  # Two levels below
        else:
            return 25.0  # More than two levels below
    
    def generate_recommendation(self, overall_score: float) -> str:
        """Generate hiring recommendation based on overall score"""
        if overall_score >= 80:
            return "Highly Recommended"
        elif overall_score >= 65:
            return "Recommended"
        elif overall_score >= 50:
            return "Maybe"
        else:
            return "Not Recommended"
    
    def generate_notes(self, skill_match: Dict, experience_score: float, 
                      education_score: float) -> str:
        """Generate detailed notes about the candidate"""
        notes = []
        
        # Skill notes
        if skill_match['required_score'] >= 80:
            notes.append("✓ Strong skill match with required skills")
        elif skill_match['required_score'] >= 60:
            notes.append("• Moderate skill match, some training may be needed")
        else:
            notes.append("✗ Significant skill gaps in required areas")
        
        # Experience notes
        if experience_score >= 100:
            notes.append("✓ Meets or exceeds experience requirements")
        elif experience_score >= 75:
            notes.append("• Close to experience requirements")
        else:
            notes.append("✗ Below experience requirements")
        
        # Education notes
        if education_score >= 100:
            notes.append("✓ Meets education requirements")
        elif education_score >= 75:
            notes.append("• Education level is acceptable")
        else:
            notes.append("✗ Below required education level")
        
        return " | ".join(notes)
    
    def screen_resume(self, resume_data: Dict, job_data: Dict) -> Dict:
        """
        Perform complete resume screening
        
        Args:
            resume_data: Dictionary with resume information
            job_data: Dictionary with job description information
        
        Returns:
            Dictionary with screening results
        """
        # Calculate skill match
        skill_match = self.calculate_skill_match(
            resume_data.get('skills', []),
            job_data.get('required_skills', []),
            job_data.get('preferred_skills', [])
        )
        
        # Calculate text similarity
        text_similarity = self.calculate_text_similarity(
            resume_data.get('text', ''),
            job_data.get('description', '')
        )
        
        # Calculate experience score
        experience_score = self.calculate_experience_score(
            resume_data.get('experience_years', 0),
            job_data.get('min_experience', 0)
        )
        
        # Calculate education score
        education_score = self.calculate_education_score(
            resume_data.get('education', 'Not Specified'),
            job_data.get('education_required', 'Not Specified')
        )
        
        # Calculate overall score (weighted average)
        overall_score = (
            skill_match['overall_score'] * 0.40 +  # 40% weight on skills
            text_similarity * 0.25 +                # 25% weight on text similarity
            experience_score * 0.20 +               # 20% weight on experience
            education_score * 0.15                  # 15% weight on education
        )
        
        # Cap overall score at 100
        overall_score = min(overall_score, 100)
        
        # Generate recommendation
        recommendation = self.generate_recommendation(overall_score)
        
        # Generate notes
        notes = self.generate_notes(skill_match, experience_score, education_score)
        
        return {
            'overall_score': overall_score,
            'skill_match_score': skill_match['overall_score'],
            'text_similarity_score': text_similarity,
            'experience_score': min(experience_score, 100),  # Cap at 100 for display
            'education_score': education_score,
            'matched_skills': skill_match['matched_required'] + skill_match['matched_preferred'],
            'missing_skills': skill_match['missing_required'] + skill_match['missing_preferred'],
            'skill_gap_analysis': {
                'required_matched': skill_match['matched_required'],
                'required_missing': skill_match['missing_required'],
                'preferred_matched': skill_match['matched_preferred'],
                'preferred_missing': skill_match['missing_preferred'],
                'total_matched': skill_match['total_matched'],
                'total_missing': skill_match['total_missing']
            },
            'recommendation': recommendation,
            'notes': notes
        }
