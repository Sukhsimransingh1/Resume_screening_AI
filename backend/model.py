from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')
print("Loaded model:", model)
def calculate_similarity(resume_text: str, jd_text: str) -> float:
    if not resume_text.strip() or not jd_text.strip():
        return 0.0

    embeddings = model.encode(
        [resume_text, jd_text],
        normalize_embeddings=True
    )

    # Dot product similarity (since normalized, same as cosine)
    score = np.dot(embeddings[0], embeddings[1])

    return round(score * 100, 2)