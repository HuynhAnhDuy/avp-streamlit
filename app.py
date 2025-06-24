# app.py – Streamlit AVP predictor demo

import streamlit as st
from main import predict
from utils import VIRUS_LABELS

st.set_page_config(page_title="AVP & Virus-specific Predictor", layout="centered")

st.title("🔬 Antiviral Peptide Prediction")
st.write("This application uses a BiLSTM model with k-mer encoding to predict general AVPs and 12 virus-specific activities.")

sequence = st.text_input("Enter a peptide sequence:")

threshold = st.slider("AVP probability threshold", min_value=0.1, max_value=0.9, value=0.5, step=0.05)

if st.button("Predict"):
    if not sequence:
        st.warning("Please enter a peptide sequence.")
    else:
        avp_prob, virus_probs = predict(sequence.strip(), threshold)

        st.markdown(f"### 🔍 General AVP Prediction:")
        st.write(f"**AVP Probability:** `{avp_prob:.3f}`")
        if avp_prob >= threshold:
            st.success("✅ Likely antiviral peptide")
        else:
            st.error("❌ Not an antiviral peptide")

        if avp_prob >= threshold:
            st.markdown("### 🦠 Virus-specific Prediction (prob ≥ 0.5):")
            results = []
            for virus, prob in zip(VIRUS_LABELS, virus_probs):
                if prob is not None and prob >= 0.5:
                    results.append((virus, prob))

            if results:
                results.sort(key=lambda x: x[1], reverse=True)
                for virus, prob in results:
                    st.write(f"- **{virus}**: `{prob:.3f}`")
            else:
                st.info("No virus-specific predictions ≥ 0.5")
import pandas as pd
import io

st.markdown("---")
st.subheader("📄 Or upload a CSV file")

uploaded_file = st.file_uploader("Upload a CSV file with a 'sequence' column", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        if "sequence" not in df.columns:
            st.error("CSV must have a column named 'sequence'.")
        else:
            st.success(f"✅ Loaded {len(df)} sequences from CSV.")
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

                # Hiển thị bảng kết quả
                st.dataframe(result_df)

                # Chuẩn bị file download
                csv = result_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download result as CSV",
                    data=csv,
                    file_name="avp_prediction_result.csv",
                    mime="text/csv",
                )
    except Exception as e:
        st.error(f"❌ Error reading CSV: {e}")

import streamlit as st, sys
st.write("🔎 Python version used:", sys.version)
