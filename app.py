# app.py – Enhanced AVP Predictor with UI improvements

import streamlit as st
from main import predict
from utils import VIRUS_LABELS
import pandas as pd
import io
import sys
from PIL import Image

st.set_page_config(page_title="AVP & Virus-specific Predictor", layout="centered")

# === Virus Descriptions ===
VIRUS_DESCRIPTIONS = {
    "HCV": "Hepatitis C Virus",
    "HSV1": "Herpes Simplex Virus Type 1",
    "DENV2": "Dengue Virus Type 2",
    "RSV": "Respiratory Syncytial Virus A",
    "INFVA": "Influenza A Virus",
    "SNV": "Sin Nombre Virus",
    "HPIV3": "Human Parainfluenza Virus Type 3",
    "FIV": "Feline Immunodeficiency Virus",
    "SARS": "SARS Coronavirus 2",
    "ANDV": "Andes Virus",
    "VACV": "Vaccinia Virus",
    "HBV": "Hepatitis B Virus"
}
# === Header & Intro ===
st.title("🧬 AVP & Virus-specific Predictor")
st.markdown("""
This web server uses a deep learning model to predict antiviral peptides (AVPs) and their virus-specific activity.

**Model:** BiLSTM with k-mer representation  
**Developers:** Huynh Anh Duy*, Tarapong Srisongkram**  
**Affiliations:** Can Tho University*, Khon Kaen University**  
""")

# === Sidebar Instructions ===
with st.sidebar:
    st.header("🧾 Instructions")
    st.markdown("""
    1. Paste a peptide sequence or upload a CSV file.
    2. Adjust the prediction threshold if needed.
    3. Click **Predict** or **Run batch prediction**.
    4. Download the results.
    """)
    st.subheader("📌 Virus Targets")
    for label in VIRUS_LABELS:
        st.markdown(f"- **{label}**: {VIRUS_DESCRIPTIONS.get(label, 'Unknown')}")

# === Sequence Input ===
st.markdown("---")
st.subheader("🔎 Predict from single sequence")

sequence = st.text_input("Enter a peptide sequence:")
threshold = st.slider("AVP probability threshold", min_value=0.1, max_value=0.9, value=0.5, step=0.05)

if st.button("Predict"):
    if not sequence:
        st.warning("Please enter a peptide sequence.")
    else:
        avp_prob, virus_probs = predict(sequence.strip(), threshold)

        st.markdown("### ✅ General AVP Prediction:")
        st.write(f"**AVP Probability:** `{avp_prob:.3f}`")
        if avp_prob >= threshold:
            st.success("Likely antiviral peptide")
        else:
            st.error("Not an antiviral peptide")

        if avp_prob >= threshold:
            st.markdown("### 🦠 Virus-specific Prediction (prob ≥ 0.5):")
            results = [(v, p) for v, p in zip(VIRUS_LABELS, virus_probs) if p is not None and p >= 0.5]
            if results:
                results.sort(key=lambda x: x[1], reverse=True)
                for virus, prob in results:
                    st.write(f"- **{virus}**: `{prob:.3f}`")
            else:
                st.info("No virus-specific predictions ≥ 0.5")

# === File Upload Batch Prediction ===
st.markdown("---")
st.subheader("📄 Upload CSV for batch prediction")

uploaded_file = st.file_uploader("Upload a CSV file with a 'sequence' column", type=["csv"])
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        if "sequence" not in df.columns:
            st.error("CSV must contain a column named 'sequence'.")
        else:
            st.success(f"✅ Loaded {len(df)} sequences.")
            if st.button("Run batch prediction"):
                output_rows = []
                for seq in df["sequence"]:
                    avp_prob, virus_probs = predict(seq.strip(), threshold)
                    row = {
                        "sequence": seq,
                        "AVP_prob": round(avp_prob, 3),
                        "AVP_candidate": "Yes" if avp_prob >= threshold else "-"
                    }
                    for vname, prob in zip(VIRUS_LABELS, virus_probs):
                        row[vname] = round(prob, 3) if prob is not None else "-"
                    output_rows.append(row)

                result_df = pd.DataFrame(output_rows)
                st.success("✅ Prediction complete!")
                st.dataframe(result_df)

                csv = result_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download results as CSV",
                    data=csv,
                    file_name="avp_prediction_results.csv",
                    mime="text/csv",
                )
    except Exception as e:
        st.error(f"❌ Error reading CSV: {e}")

# === Author Section ===
st.markdown("---")
st.subheader("👨‍🔬 About the Authors")

col1, col2 = st.columns(2)

with col1:
    image1 = Image.open("assets/duy.jpg")
    st.image(image1, caption="Huynh Anh Duy", width=160)
    st.markdown("""
    **Huynh Anh Duy**  
    Can Tho University, Vietnam  
    PhD Candidate, Khon Kaen University, Thailand
    *Cheminformatics, QSAR Modeling, Computational Drug Discovery and Toxicity Prediction*  
    📧 [huynhanhduy.h@kkumail.com](mailto:huynhanhduy.h@kkumail.com) [haduy@ctu.edu.vn](mailto:haduy@ctu.edu.vn)
    """)

with col2:
    image2 = Image.open("assets/tarasi.png")
    st.image(image2, caption="Tarapong Srisongkram", width=160)
    st.markdown("""
    **Asst Prof. Dr. Tarapong Srisongkram**  
    Faculty of Pharmaceutical Sciences  
    Khon Kaen University, Thailand  
    *Cheminformatics, QSAR Modeling, Computational Drug Discovery and Toxicity Prediction*  
    📧 [tarasri@kku.ac.th](mailto:tarasri@kku.ac.th)
    """)

# === Footer Debug ===
st.markdown("---")
st.caption(f"Python version: {sys.version}")
