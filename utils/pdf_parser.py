import PyPDF2
import pdfplumber
import docx
import re
from typing import Dict, List, Optional

class ResumeParser:
    """Parse resumes from PDF and DOCX files"""
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """Extract text from PDF file using multiple methods"""
        text = ""
        
        # Try pdfplumber first (better for complex PDFs)
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"pdfplumber failed: {e}")
        
        # Fallback to PyPDF2 if pdfplumber fails
        if not text.strip():
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            except Exception as e:
                print(f"PyPDF2 failed: {e}")
        
        return text.strip()
    
    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except Exception as e:
            print(f"DOCX extraction failed: {e}")
            return ""
    
    @staticmethod
    def extract_text(file_path: str) -> str:
        """Extract text based on file extension"""
        if file_path.lower().endswith('.pdf'):
            return ResumeParser.extract_text_from_pdf(file_path)
        elif file_path.lower().endswith(('.docx', '.doc')):
            return ResumeParser.extract_text_from_docx(file_path)
        else:
            raise ValueError("Unsupported file format")
    
    @staticmethod
    def extract_email(text: str) -> Optional[str]:
        """Extract email address from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else None
    
    @staticmethod
    def extract_phone(text: str) -> Optional[str]:
        """Extract phone number from text"""
        # Match various phone formats
        phone_patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\d{10}'
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, text)
            if phones:
                return phones[0]
        return None
    
    @staticmethod
    def extract_name(text: str) -> Optional[str]:
        """Extract candidate name (usually first line or after specific keywords)"""
        lines = text.split('\n')
        
        # Try to find name in first few lines
        for line in lines[:5]:
            line = line.strip()
            # Skip empty lines and common headers
            if line and len(line.split()) <= 4 and not any(keyword in line.lower() for keyword in 
                ['resume', 'cv', 'curriculum', 'vitae', 'email', 'phone', 'address']):
                # Check if it looks like a name (2-4 words, mostly alphabetic)
                words = line.split()
                if 1 <= len(words) <= 4 and all(word.replace('.', '').isalpha() for word in words):
                    return line
        
        return None
    
    @staticmethod
    def extract_experience_years(text: str) -> float:
        """Extract years of experience from text"""
        text_lower = text.lower()
        
        # Patterns to match experience
        patterns = [
            r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
            r'experience[:\s]+(\d+)\+?\s*years?',
            r'(\d+)\+?\s*yrs?\s+(?:of\s+)?experience',
        ]
        
        years = []
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            years.extend([int(match) for match in matches])
        
        # Also try to count job positions with dates
        date_ranges = re.findall(r'(\d{4})\s*[-–]\s*(\d{4}|present|current)', text_lower)
        if date_ranges:
            total_years = 0
            for start, end in date_ranges:
                end_year = 2024 if end in ['present', 'current'] else int(end)
                total_years += end_year - int(start)
            years.append(total_years)
        
        return max(years) if years else 0.0
    
    @staticmethod
    def extract_education(text: str) -> str:
        """Extract highest education level"""
        text_lower = text.lower()
        
        education_levels = {
            'phd': ['phd', 'ph.d', 'doctorate', 'doctoral'],
            'masters': ['master', 'msc', 'm.sc', 'ma', 'm.a', 'mba', 'm.b.a', 'mtech', 'm.tech'],
            'bachelors': ['bachelor', 'bsc', 'b.sc', 'ba', 'b.a', 'btech', 'b.tech', 'be', 'b.e'],
            'diploma': ['diploma', 'associate'],
            'high school': ['high school', 'secondary', '12th', 'xii']
        }
        
        for level, keywords in education_levels.items():
            if any(keyword in text_lower for keyword in keywords):
                return level.title()
        
        return 'Not Specified'
    
    @staticmethod
    def extract_skills(text: str, skill_list: List[str]) -> List[str]:
        """Extract skills from text based on predefined skill list"""
        text_lower = text.lower()
        found_skills = []
        
        for skill in skill_list:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill)
        
        return list(set(found_skills))  # Remove duplicates
    
    @staticmethod
    def parse_resume(file_path: str, skill_list: List[str]) -> Dict:
        """Parse resume and extract all information"""
        text = ResumeParser.extract_text(file_path)
        
        return {
            'text': text,
            'name': ResumeParser.extract_name(text),
            'email': ResumeParser.extract_email(text),
            'phone': ResumeParser.extract_phone(text),
            'skills': ResumeParser.extract_skills(text, skill_list),
            'experience_years': ResumeParser.extract_experience_years(text),
            'education': ResumeParser.extract_education(text)
        }
