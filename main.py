# main.py – AVP & Virus-specific predictor (TensorFlow/Keras)
# ----------------------------------------------------------
# Usage:
#   python main.py KLWKKLLKKLLKAA
#   python main.py --csv peptides.csv
# ----------------------------------------------------------

import argparse
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

from utils import (
    preprocess_sequence,
    VIRUS_LABELS,
)

ROOT_DIR = Path(__file__).parent
VECTOR_PREFIX = "kmer_vectorizer_"

# ----------------------------------------------------------
# 1. Load model & vectorizer at startup
# ----------------------------------------------------------
def load_models_and_vectorizers():
    general_model = load_model(ROOT_DIR / "models"/ "avp_general.keras", compile=False)

    virus_models, virus_vecs = [], []
    for i, virus in enumerate(VIRUS_LABELS):
        model_path = ROOT_DIR /"models"/ f"virus_{i}_{virus.lower()}.keras"
        if not model_path.exists():
            raise FileNotFoundError(model_path)
        virus_models.append(load_model(model_path, compile=False))

        vec_path = ROOT_DIR/"vectorizers" / f"{VECTOR_PREFIX}{virus.lower()}.pkl"
        if not vec_path.exists():
            raise FileNotFoundError(vec_path)
        virus_vecs.append(joblib.load(vec_path))

    print("✅ Loaded general model, 12 virus models & vectorizers")
    return general_model, virus_models, virus_vecs

GENERAL_MODEL, VIRUS_MODELS, VIRUS_VECS = load_models_and_vectorizers()

# ----------------------------------------------------------
# 2. Encode sequence using k-mer vectorizer
# ----------------------------------------------------------
def preprocess_sequence_kmer(seq: str, vectorizer, k: int = 3) -> np.ndarray:
    kmers = [seq[i:i + k] for i in range(len(seq) - k + 1)]
    sentence = " ".join(kmers)
    vec = vectorizer.transform([sentence]).toarray().astype(np.float32)
    return vec.reshape((1, 1, -1))

# ----------------------------------------------------------
# 3. Prediction logic
# ----------------------------------------------------------
def predict(seq: str, threshold: float = 0.5):
    x_general = preprocess_sequence(seq)
    avp_prob = float(GENERAL_MODEL.predict(x_general, verbose=0).ravel()[0])

    virus_probs = []
    if avp_prob >= threshold:
        for model, vec in zip(VIRUS_MODELS, VIRUS_VECS):
            x_v = preprocess_sequence_kmer(seq, vec)
            virus_probs.append(float(model.predict(x_v, verbose=0).ravel()[0]))
    else:
        virus_probs = [None] * len(VIRUS_LABELS)

    return avp_prob, virus_probs

# ----------------------------------------------------------
# 4. CLI entrypoint
# ----------------------------------------------------------
def cli():
    parser = argparse.ArgumentParser(
        description="AVP & virus-specific predictor",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("sequence", nargs="?", help="Peptide sequence, e.g. KLWKKLLKKLLKAA")
    parser.add_argument("--csv", type=str, help="CSV file with a 'sequence' column")
    parser.add_argument("--threshold", type=float, default=0.5,
                        help="AVP probability threshold before virus-specific models run")
    args = parser.parse_args()

    if args.csv:
        df = pd.read_csv(args.csv)
        if "sequence" not in df.columns:
            print("CSV must have a 'sequence' column"); return
        out = []
        for s in df["sequence"]:
            avp_prob, virus_probs = predict(s, args.threshold)
            row = {
                "sequence": s,
                "AVP_prob": round(avp_prob, 3),
                "AVP_candidate": "Yes" if avp_prob >= args.threshold else "-"
            }
            for vname, prob in zip(VIRUS_LABELS, virus_probs):
                row[vname] = round(prob, 3) if prob is not None else "-"
            out.append(row)
        out_df = pd.DataFrame(out)
        out_path = ROOT_DIR / "outputs" / "predicted_output.csv"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_df.to_csv(out_path, index=False)
        print(f"\n✅ Saved CSV → {out_path.resolve()}")
    elif args.sequence:
        avp_prob, virus_probs = predict(args.sequence, args.threshold)
        print(f"\nSequence: {args.sequence}")
        print(f"(1) AVP probability: {avp_prob:.3f}")

        if avp_prob >= args.threshold:
            print("→ Antiviral peptide candidate (probabilities ≥ 0.5)")
            filtered = [(v, p) for v, p in zip(VIRUS_LABELS, virus_probs) if p >= 0.5]
            filtered.sort(key=lambda x: x[1], reverse=True)
            if filtered:
                print("(2) Virus-specific probabilities ≥ 0.5:")
                for v, p in filtered:
                    print(f"  {v:<10}: {p:.3f}")
            else:
                print("No virus-specific probabilities ≥ 0.5.")
        else:
            print("→ Not an AVP candidate (below threshold)")
    else:
        parser.print_help()

# ----------------------------------------------------------
if __name__ == "__main__":
    cli()
