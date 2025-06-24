# utils.py – Universal k-mer preprocessing for AVP + virus-specific models
import numpy as np
from pathlib import Path
import joblib

# Virus labels – must match model order: virus_0_*.keras → virus_11_*.keras
VIRUS_LABELS = [
    "HCV", "HSV1", "DENV2", "RSV", "INFVA", "SNV",
    "HPIV3", "FIV", "SARS", "ANDV", "VACV", "HBV",
]

_KMER = 3  # k-mer length used in training
PACKAGE_DIR = Path(__file__).resolve().parent

# Cache loaded vectorizers to avoid re-loading
_VECTOR_CACHE = {}

def _generate_kmers(seq: str, k: int = _KMER):
    return [seq[i:i + k] for i in range(len(seq) - k + 1)]

def load_vectorizer(source: str = "general"):
    """
    Load vectorizer:
    - source="general" → kmer_vectorizer_general.pkl
    - source="hcv", "sars", ... → kmer_vectorizer_hcv.pkl, ...
    """
    if source not in _VECTOR_CACHE:
        vec_path = PACKAGE_DIR / "vectorizers" /f"kmer_vectorizer_{source.lower()}.pkl"
        if not vec_path.exists():
            raise FileNotFoundError(f"Missing vectorizer: {vec_path}")
        _VECTOR_CACHE[source] = joblib.load(vec_path)
    return _VECTOR_CACHE[source]

def preprocess_sequence(seq: str, vectorizer_source: str = "general"):
    """
    Convert peptide sequence to shape (1, 1, num_features).
    `vectorizer_source` can be "general" or virus name ("hcv", "sars", ...).
    """
    seq = seq.upper()
    sentence = " ".join(_generate_kmers(seq))
    vectorizer = load_vectorizer(vectorizer_source)
    vec = vectorizer.transform([sentence]).toarray().astype(np.float32)
    return vec.reshape((1, 1, -1))
