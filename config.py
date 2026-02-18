import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///resume_screening.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload settings
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    
    # ML Model settings
    MODEL_PATH = 'models'
    VECTORIZER_PATH = os.path.join(MODEL_PATH, 'vectorizer.pkl')
    
    # Skills database
    COMMON_SKILLS = [
        # Programming Languages
        'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'go',
        'rust', 'typescript', 'scala', 'r', 'matlab', 'perl', 'shell', 'bash',
        
        # Web Technologies
        'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask',
        'spring', 'asp.net', 'jquery', 'bootstrap', 'tailwind', 'sass', 'webpack',
        
        # Databases
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite', 'cassandra',
        'dynamodb', 'elasticsearch', 'firebase', 'mariadb',
        
        # Cloud & DevOps
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'gitlab', 'github actions',
        'terraform', 'ansible', 'ci/cd', 'linux', 'unix', 'nginx', 'apache',
        
        # Data Science & ML
        'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'keras', 'scikit-learn',
        'pandas', 'numpy', 'data analysis', 'data visualization', 'tableau', 'power bi',
        'nlp', 'computer vision', 'neural networks', 'ai',
        
        # Mobile Development
        'android', 'ios', 'react native', 'flutter', 'xamarin', 'mobile development',
        
        # Other Technologies
        'git', 'rest api', 'graphql', 'microservices', 'agile', 'scrum', 'jira',
        'testing', 'unit testing', 'selenium', 'jest', 'pytest', 'api development',
        'oauth', 'jwt', 'security', 'encryption', 'blockchain', 'solidity',
        
        # Soft Skills
        'communication', 'leadership', 'teamwork', 'problem solving', 'critical thinking',
        'project management', 'time management', 'analytical skills', 'creativity'
    ]
