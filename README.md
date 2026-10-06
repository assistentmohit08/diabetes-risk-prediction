# Diabetes Risk Prediction

Web app that estimates diabetes risk from 8 health markers using Logistic Regression
trained on the Pima Indians Diabetes dataset.

## Results
| Metric | Value |
|---|---|
| Test Accuracy | <your value> |
| Test ROC-AUC | <your value> |
| 5-fold CV ROC-AUC | <your value> |

## Tech Stack
Python, pandas, scikit-learn, Flask, HTML/CSS/JavaScript, Google Colab

## Approach
1. EDA: found hidden missing values (zeros in Glucose, BloodPressure, SkinThickness, Insulin, BMI).
2. Stratified train/test split before any preprocessing to avoid data leakage.
3. scikit-learn Pipeline: median imputation -> standard scaling -> Logistic Regression.
4. Evaluated with ROC-AUC, recall and confusion matrix (data is imbalanced, about 65/35).
5. Served via Flask REST API with input validation.

## Run locally
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    python app/app.py
Open http://127.0.0.1:5000

## API
POST /predict with JSON body of the 8 features.
Glucose and BMI are required. BloodPressure, SkinThickness and Insulin are optional.

## Limitations
- Small dataset (768 rows), all female patients of Pima Indian heritage, aged 21+.
- Risk-level cutoffs (0.30 / 0.60) are illustrative, not medically validated.
- Educational project, not a medical device.