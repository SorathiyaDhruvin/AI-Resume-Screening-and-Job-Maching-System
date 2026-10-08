import re

class SkillExtractor:
    # A simple known taxonomy for demo purposes.
    # In a real scenario, this would come from the database `skills` table.
    KNOWN_SKILLS = [
        "java", "python", "c++", "javascript", "typescript", "react", "html", "css",
        "spring boot", "fastapi", "node.js", "express", "postgresql", "mysql", 
        "mongodb", "machine learning", "nlp", "scikit-learn", "tensorflow", 
        "pytorch", "sentence transformers", "aws", "docker", "git", "github",
        "sql", "dsa", "kubernetes", "django", "flask", "vue.js", "angular"
    ]

    @classmethod
    def extract_skills(cls, text: str):
        text_lower = text.lower()
        extracted = set()
        for skill in cls.KNOWN_SKILLS:
            # use regex word boundary to avoid partial matches
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                extracted.add(skill)
        return list(extracted)
