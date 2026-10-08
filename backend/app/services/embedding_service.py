from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from app.core.config import settings

class EmbeddingService:
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            cls._model = SentenceTransformer(settings.MODEL_NAME, device="cpu")
        return cls._model

    @classmethod
    def get_embedding(cls, text: str):
        if not text:
            return np.zeros(384) # Default size for all-MiniLM-L6-v2
        model = cls.get_model()
        return model.encode(text)

    @classmethod
    def calculate_similarity(cls, text1: str, text2: str) -> float:
        emb1 = cls.get_embedding(text1)
        emb2 = cls.get_embedding(text2)
        # Reshape for sklearn
        emb1_2d = np.array(emb1).reshape(1, -1)
        emb2_2d = np.array(emb2).reshape(1, -1)
        similarity = cosine_similarity(emb1_2d, emb2_2d)[0][0]
        return float(similarity)
