from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime

from config import Config
from models import db, Resume, JobDescription, Screening
from utils.pdf_parser import ResumeParser
from utils.ml_matcher import ResumeJobMatcher

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
CORS(app)
db.init_app(app)

# Create upload and model directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['MODEL_PATH'], exist_ok=True)

# Initialize ML matcher
matcher = ResumeJobMatcher()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# ==================== Routes ====================

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'AI Resume Screening System is running',
        'timestamp': datetime.utcnow().isoformat()
    })


@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
    """Upload and parse resume"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only PDF and DOCX allowed'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        # Parse resume
        parsed_data = ResumeParser.parse_resume(file_path, Config.COMMON_SKILLS)
        
        # Save to database
        resume = Resume(
            filename=unique_filename,
            original_filename=filename,
            file_path=file_path,
            extracted_text=parsed_data['text'],
            candidate_name=parsed_data['name'],
            candidate_email=parsed_data['email'],
            candidate_phone=parsed_data['phone'],
            skills_found=json.dumps(parsed_data['skills']),
            experience_years=parsed_data['experience_years'],
            education_level=parsed_data['education']
        )
        
        db.session.add(resume)
        db.session.commit()
        
        return jsonify({
            'message': 'Resume uploaded and parsed successfully',
            'resume': resume.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/resumes', methods=['GET'])
def get_resumes():
    """Get all resumes"""
    try:
        resumes = Resume.query.order_by(Resume.uploaded_at.desc()).all()
        return jsonify({
            'resumes': [resume.to_dict() for resume in resumes],
            'total': len(resumes)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/resumes/<int:resume_id>', methods=['GET'])
def get_resume(resume_id):
    """Get specific resume"""
    try:
        resume = Resume.query.get_or_404(resume_id)
        return jsonify({'resume': resume.to_dict()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/resumes/<int:resume_id>', methods=['DELETE'])
def delete_resume(resume_id):
    """Delete resume"""
    try:
        resume = Resume.query.get_or_404(resume_id)
        
        # Delete file
        if os.path.exists(resume.file_path):
            os.remove(resume.file_path)
        
        db.session.delete(resume)
        db.session.commit()
        
        return jsonify({'message': 'Resume deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/jobs', methods=['POST'])
def create_job():
    """Create job description"""
    try:
        data = request.get_json()
        
        job = JobDescription(
            title=data['title'],
            description=data['description'],
            required_skills=json.dumps(data.get('required_skills', [])),
            preferred_skills=json.dumps(data.get('preferred_skills', [])),
            min_experience=data.get('min_experience', 0),
            education_required=data.get('education_required', 'Not Specified')
        )
        
        db.session.add(job)
        db.session.commit()
        
        return jsonify({
            'message': 'Job description created successfully',
            'job': job.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Get all job descriptions"""
    try:
        jobs = JobDescription.query.order_by(JobDescription.created_at.desc()).all()
        return jsonify({
            'jobs': [job.to_dict() for job in jobs],
            'total': len(jobs)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Get specific job description"""
    try:
        job = JobDescription.query.get_or_404(job_id)
        return jsonify({'job': job.to_dict()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    """Delete job description"""
    try:
        job = JobDescription.query.get_or_404(job_id)
        db.session.delete(job)
        db.session.commit()
        
        return jsonify({'message': 'Job description deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/screen', methods=['POST'])
def screen_resume():
    """Screen resume against job description"""
    try:
        data = request.get_json()
        resume_id = data.get('resume_id')
        job_id = data.get('job_id')
        
        if not resume_id or not job_id:
            return jsonify({'error': 'Resume ID and Job ID are required'}), 400
        
        # Get resume and job
        resume = Resume.query.get_or_404(resume_id)
        job = JobDescription.query.get_or_404(job_id)
        
        # Prepare data for matching
        resume_data = {
            'text': resume.extracted_text,
            'skills': json.loads(resume.skills_found) if resume.skills_found else [],
            'experience_years': resume.experience_years or 0,
            'education': resume.education_level or 'Not Specified'
        }
        
        job_data = {
            'description': job.description,
            'required_skills': json.loads(job.required_skills) if job.required_skills else [],
            'preferred_skills': json.loads(job.preferred_skills) if job.preferred_skills else [],
            'min_experience': job.min_experience or 0,
            'education_required': job.education_required or 'Not Specified'
        }
        
        # Perform screening
        results = matcher.screen_resume(resume_data, job_data)
        
        # Save screening results
        screening = Screening(
            resume_id=resume_id,
            job_id=job_id,
            overall_score=results['overall_score'],
            skill_match_score=results['skill_match_score'],
            experience_score=results['experience_score'],
            education_score=results['education_score'],
            text_similarity_score=results['text_similarity_score'],
            matched_skills=json.dumps(results['matched_skills']),
            missing_skills=json.dumps(results['missing_skills']),
            skill_gap_analysis=json.dumps(results['skill_gap_analysis']),
            recommendation=results['recommendation'],
            notes=results['notes']
        )
        
        db.session.add(screening)
        db.session.commit()
        
        return jsonify({
            'message': 'Resume screened successfully',
            'screening': screening.to_dict(),
            'resume': resume.to_dict(),
            'job': job.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/screenings', methods=['GET'])
def get_screenings():
    """Get all screening results"""
    try:
        screenings = Screening.query.order_by(Screening.screened_at.desc()).all()
        
        results = []
        for screening in screenings:
            result = screening.to_dict()
            result['resume'] = screening.resume.to_dict()
            result['job'] = screening.job.to_dict()
            results.append(result)
        
        return jsonify({
            'screenings': results,
            'total': len(results)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/screenings/<int:screening_id>', methods=['GET'])
def get_screening(screening_id):
    """Get specific screening result"""
    try:
        screening = Screening.query.get_or_404(screening_id)
        
        result = screening.to_dict()
        result['resume'] = screening.resume.to_dict()
        result['job'] = screening.job.to_dict()
        
        return jsonify({'screening': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get analytics data"""
    try:
        total_resumes = Resume.query.count()
        total_jobs = JobDescription.query.count()
        total_screenings = Screening.query.count()
        
        # Average scores
        avg_overall = db.session.query(db.func.avg(Screening.overall_score)).scalar() or 0
        avg_skill = db.session.query(db.func.avg(Screening.skill_match_score)).scalar() or 0
        
        # Recommendation distribution
        recommendations = db.session.query(
            Screening.recommendation,
            db.func.count(Screening.id)
        ).group_by(Screening.recommendation).all()
        
        return jsonify({
            'total_resumes': total_resumes,
            'total_jobs': total_jobs,
            'total_screenings': total_screenings,
            'average_overall_score': round(avg_overall, 2),
            'average_skill_score': round(avg_skill, 2),
            'recommendations': {rec: count for rec, count in recommendations}
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Initialize database
with app.app_context():
    db.create_all()
    print("✅ Database initialized successfully")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
