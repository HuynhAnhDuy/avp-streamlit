# 🧬 AVP PREDICTOR TOOL – USER GUIDE (Streamlit Version)

## Overview
This web-based tool predicts whether a peptide sequence has antiviral activity (AVP) and estimates its potential to inhibit specific virus types.

It is powered by a deep learning BiLSTM model trained on curated antiviral peptide datasets using k-mer encoding.  
The tool is implemented in Python and deployed as an interactive **Streamlit application**.

---

## 🔑 Key Features

- Predicts **general AVP probability** for input peptide sequences
- If AVP probability ≥ threshold, provides **virus-specific predictions** for 12 viruses
- Supports:
  - ✅ Single peptide input (via text box)
  - ✅ Batch prediction (via `.csv` upload)
- Downloadable `.csv` output for batch analysis
- Simple, browser-based usage – no installation required

---

## 🚀 Getting Started

🔗 **Access the web application here**:  
👉 [https://your-app-name.streamlit.app](https://your-app-name.streamlit.app)

> Replace the above link with your actual Streamlit URL

---

### ✅ Option 1: Single Sequence Prediction

1. Enter your peptide sequence (e.g. `KLWKKLLKKLLKAA`)
2. Adjust the **AVP probability threshold** (default is `0.5`)
3. Click **"Predict"**
4. The results will include:
   - AVP probability
   - Whether the peptide is likely antiviral
   - Virus-specific predictions if AVP ≥ threshold

---

### ✅ Option 2: Batch Prediction via CSV Upload

1. Prepare a `.csv` file with the following format:


2. Upload the file using the **Upload section**
3. Click **"Run batch prediction"**
4. A result table will be displayed and available for **download as `.csv`**

---

## 📤 Output Examples

### ✅ Terminal-like Output (Single Prediction)
AVP probability: 0.823
Likely virus targets (prob ≥ 0.5):
DENV2 : 0.766
SNV : 0.661
VACV : 0.534


---

### ✅ Batch CSV Output Example

| sequence        | AVP_prob | AVP_candidate | DENV2 | SNV  | VACV | ... |
|-----------------|----------|---------------|-------|------|------|-----|
| KLWKKLLKKLLKAA  | 0.823    | Yes           | 0.766 | 0.66 | 0.53 | ... |
| GLFDIIKKIAESF   | 0.233    | -             |   -   |  -   |  -   | ... |

---

## 🦠 Supported Virus Targets (12)

The model provides predictions for the following viruses:

- HCV (Hepatitis C Virus)
- HSV1 (Herpes Simplex Virus Type 1)
- DENV2 (Dengue Virus Type 2)
- RSV (Respiratory Syncytial Virus)
- INFVA (Influenza A)
- SNV (Sin Nombre Virus)
- HPIV3 (Human Parainfluenza Virus 3)
- FIV (Feline Immunodeficiency Virus)
- SARS-CoV2 (COVID-19)
- ANDV (Andes Virus)
- VACV (Vaccinia Virus)
- HBV (Hepatitis B Virus)

---

## 🛠️ Technology Stack

- Python 3
- TensorFlow / Keras
- Scikit-learn
- Pandas / NumPy
- Streamlit

---

## 📬 Contact & Support

- **Lead Developer**: Huynh Anh Duy  
- **Research Advisor**: Tarapong Srisongkram  
- **Emails**: `haduy@ctu.edu.vn`, `tarasri@kku.ac.th`  
- **Institution**: Khon Kaen University, Thailand / Can Tho University, Vietnam

---

## 📌 Version Info

- **Version**: 1.0  
- **Last updated**: June 2025  
- **License**: Academic / Research use only

---

**Thank you for using AVP Predictor Tool!**
