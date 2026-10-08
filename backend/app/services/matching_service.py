from typing import List, Dict

class MatchingService:
    @staticmethod
    def calculate_skill_match(required_skills: List[str], candidate_skills: List[str]) -> Dict:
        if not required_skills:
            return {"score": 1.0, "matched": [], "missing": []}
        
        req_lower = set(s.lower() for s in required_skills)
        cand_lower = set(s.lower() for s in candidate_skills)
        
        matched = list(req_lower.intersection(cand_lower))
        missing = list(req_lower.difference(cand_lower))
        
        score = len(matched) / len(req_lower)
        return {"score": score, "matched": matched, "missing": missing}

    @staticmethod
    def calculate_final_score(semantic_score: float, skill_score: float, exp_score: float = 1.0, edu_score: float = 1.0, pref_score: float = 1.0) -> float:
        # Weights
        # Semantic: 40%
        # Skill: 30%
        # Experience: 15%
        # Education: 10%
        # Preferred: 5%
        
        final = (
            (semantic_score * 0.40) +
            (skill_score * 0.30) +
            (exp_score * 0.15) +
            (edu_score * 0.10) +
            (pref_score * 0.05)
        )
        return final
