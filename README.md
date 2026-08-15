# Professional BMI Calculator

A production-quality Body Mass Index (BMI) Calculator built with Python and Streamlit. This application is designed to be user-friendly for the general public while offering detailed calculation metrics for healthcare professionals.

## Features

- **Dual Input Modes**: Supports both Metric (cm/kg) and Imperial (ft, in/lbs) units with seamless conversion.
- **Age-Aware Interpretation**: Safely handles pediatric users by avoiding inappropriate adult BMI categorizations for individuals under 18.
- **Professional View**: Provides exact calculation formulas, converted metrics, and clinical caveats for healthcare professionals.
- **Healthy Weight Range**: Calculates the approximate healthy weight range (BMI 18.5-24.9) for adult users.
- **Privacy-Focused**: Calculations are performed locally; no personal health information is stored or transmitted.

## Requirements

- Python 3.11+
- Streamlit

## Installation & Local Execution

1. **Clone the repository** (or download the files).
2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## Streamlit Deployment

This application is ready to be deployed on **Streamlit Community Cloud**:
1. Push this repository to GitHub.
2. Log in to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click "New app".
4. Select the repository, branch, and specify `app.py` as the Main file path.
5. Click "Deploy".

## Medical Disclaimer

BMI is a screening measure and does not diagnose disease or fully describe an individual's health. BMI may be interpreted differently for certain populations and circumstances. Consult a qualified healthcare professional for personalized medical advice.

This application is intended for educational and informational purposes only.
