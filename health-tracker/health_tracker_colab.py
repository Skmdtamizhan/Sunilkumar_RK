# ==============================================================================
# HEIGHT-WEIGHT HEALTH TRACKER: END-TO-END ML PIPELINE & DEPLOYMENT
# Ready for Google Colab / Jupyter / Local Python
# ==============================================================================

"""
CRITICAL FIXES APPLIED TO YOUR ORIGINAL CODE:
1. FIXED MODEL SERIALIZATION: In your original code, `dump(data, open('weight-height.pkl', 'wb'))`
   dumped the pandas DataFrame `data` instead of the trained LinearRegression `model`.
   This script correctly saves the trained models.

2. FIXED UNIT PREPROCESSING ORDER: In your original code, `x` was extracted before converting
   Height and Weight (`* 2.54` and `/ 2.205`). Because `drop()` creates a new DataFrame,
   your logistic regression model was accidentally trained on raw imperial units (inches/lbs)
   rather than metric units (cm/kg). This script cleanly converts units first.

3. ADDED PROPER TRAIN/TEST SPLIT & EVALUATION: Added stratified 80/20 train/test splitting
   and computed proper generalization metrics (Accuracy, ROC-AUC, Confusion Matrix, R², RMSE).

4. EXPORTED TO JSON FOR ZERO-BACKEND WEB DEPLOYMENT: Exported model coefficients and intercepts
   to `model_params.json` so you can deploy your models in pure JavaScript on ANY webpage
   without paying for or maintaining a Python server!
"""

import os
import json
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    mean_squared_error, r2_score
)

# ------------------------------------------------------------------------------
# STEP 1: DATA INGESTION
# ------------------------------------------------------------------------------
# In Google Colab, uncomment the next two lines to upload 'weight-height.csv':
# from google.colab import files
# uploaded = files.upload()

csv_path = 'weight-height.csv'

if not os.path.exists(csv_path):
    print(f"File '{csv_path}' not found in current directory. Checking subfolder...")
    if os.path.exists(os.path.join('health-tracker', 'weight-height.csv')):
        csv_path = os.path.join('health-tracker', 'weight-height.csv')
    else:
        raise FileNotFoundError(f"Please place '{csv_path}' in your working directory.")

data = pd.read_csv(csv_path)

print("="*70)
print("1. DATA UNDERSTANDING & PREVIEW")
print("="*70)
print(data.head())
print(f"\nDataset Shape: {data.shape} (Rows, Columns)")
print(f"Missing Values Check:\n{data.isna().sum()}\n")

# ------------------------------------------------------------------------------
# STEP 2: DATA PREPARATION & STANDARDIZATION (METRIC SYSTEM)
# ------------------------------------------------------------------------------
# Original dataset: Height in inches, Weight in pounds (lbs)
# Standard medical/scientific units: Height in cm, Weight in kg
data['Height_cm'] = data['Height'] * 2.54
data['Weight_kg'] = data['Weight'] / 2.20462

# Binary encoding: Male = 0, Female = 1
data['Gender_Code'] = data['Gender'].map({'Male': 0, 'Female': 1})

# Also compute Body Mass Index (BMI) for data exploration
data['BMI'] = data['Weight_kg'] / ((data['Height_cm'] / 100) ** 2)

print("="*70)
print("2. PREPROCESSED DATA SAMPLE (METRIC CONVERTED)")
print("="*70)
print(data[['Gender', 'Height_cm', 'Weight_kg', 'BMI', 'Gender_Code']].head())

# ------------------------------------------------------------------------------
# STEP 3: MODEL 1 - LINEAR REGRESSION (Weight from Height)
# ------------------------------------------------------------------------------
print("\n" + "="*70)
print("3. TRAINING LINEAR REGRESSION MODEL")
print("="*70)

X_reg = data[['Height_cm']]
y_reg = data['Weight_kg']

X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)

reg_model = LinearRegression()
reg_model.fit(X_train_r, y_train_r)

# Model Evaluation
y_pred_r = reg_model.predict(X_test_r)
r2 = r2_score(y_test_r, y_pred_r)
rmse = np.sqrt(mean_squared_error(y_test_r, y_pred_r))

slope = float(reg_model.coef_[0])
intercept = float(reg_model.intercept_)

print(f"Linear Regression R² Score: {r2:.4f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f} kg")
print(f"Learned Equation: Weight(kg) = {slope:.4f} * Height(cm) + ({intercept:.4f})")

# Save trained Linear Regression model to pickle
with open('weight_height_linear.pkl', 'wb') as f:
    pickle.dump(reg_model, f)
print(" Saved: 'weight_height_linear.pkl' (Fixed: saved model object, not dataframe)")

# ------------------------------------------------------------------------------
# STEP 4: MODEL 2 - LOGISTIC REGRESSION (Gender Classification)
# ------------------------------------------------------------------------------
print("\n" + "="*70)
print("4. TRAINING LOGISTIC REGRESSION MODEL (CLASSIFICATION)")
print("="*70)

X_clf = data[['Height_cm', 'Weight_kg']]
y_clf = data['Gender_Code']

X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
    X_clf, y_clf, test_size=0.2, random_state=42, stratify=y_clf
)

clf_model = LogisticRegression(random_state=42)
clf_model.fit(X_train_c, y_train_c)

# Evaluation on Unseen Test Set
y_pred_c = clf_model.predict(X_test_c)
y_pred_proba = clf_model.predict_proba(X_test_c)
acc = accuracy_score(y_test_c, y_pred_c)

coef_h = float(clf_model.coef_[0][0])
coef_w = float(clf_model.coef_[0][1])
clf_intercept = float(clf_model.intercept_[0])

print(f"Classification Test Accuracy: {acc * 100:.2f}%")
print(f"Height Coefficient: {coef_h:.4f}")
print(f"Weight Coefficient: {coef_w:.4f}")
print(f"Intercept: {clf_intercept:.4f}")

print("\nConfusion Matrix:")
cm = confusion_matrix(y_test_c, y_pred_c)
print(f"  [TN={cm[0,0]} (Male),  FP={cm[0,1]}]")
print(f"  [FN={cm[1,0]},  TP={cm[1,1]} (Female)]")

print("\nClassification Report:")
print(classification_report(y_test_c, y_pred_c, target_names=['Male', 'Female']))

# Save trained Logistic Regression model to pickle
with open('gender_classification.pkl', 'wb') as f:
    pickle.dump(clf_model, f)
print(" Saved: 'gender_classification.pkl'")

# ------------------------------------------------------------------------------
# STEP 5: EXPORT PARAMETERS TO JSON (FOR ZERO-SERVER WEB DEPLOYMENT)
# ------------------------------------------------------------------------------
print("\n" + "="*70)
print("5. EXPORTING MODEL PARAMETERS FOR WEB & JAVASCRIPT DEPLOYMENT")
print("="*70)

deploy_payload = {
    "linear_regression": {
        "slope": slope,
        "intercept": intercept,
        "r2_score": float(r2),
        "rmse_kg": float(rmse),
        "formula": f"Weight_kg = {slope:.4f} * Height_cm + ({intercept:.4f})"
    },
    "logistic_regression": {
        "coef_height": coef_h,
        "coef_weight": coef_w,
        "intercept": clf_intercept,
        "test_accuracy": float(acc),
        "formula": f"z = {coef_h:.4f}*Height_cm + {coef_w:.4f}*Weight_kg + ({clf_intercept:.4f})",
        "labels": {"0": "Male", "1": "Female"}
    },
    "health_benchmarks": {
        "who_bmi": {
            "underweight": "< 18.5",
            "normal": "18.5 - 24.9",
            "overweight": "25.0 - 29.9",
            "obese_1": "30.0 - 34.9",
            "obese_2_3": ">= 35.0"
        },
        "mifflin_st_jeor": {
            "male": "10*W(kg) + 6.25*H(cm) - 5*Age + 5",
            "female": "10*W(kg) + 6.25*H(cm) - 5*Age - 161"
        }
    }
}

with open('health_tracker_model_params.json', 'w') as f:
    json.dump(deploy_payload, f, indent=2)

print(" Saved: 'health_tracker_model_params.json'")
print("This JSON allows client-side execution in JavaScript with 0 latency and 0 server cost!")

# ------------------------------------------------------------------------------
# STEP 6: VERIFY SINGLE PREDICTION TEST
# ------------------------------------------------------------------------------
print("\n" + "="*70)
print("6. RUNNING SAMPLE INFERENCE")
print("="*70)

test_height = 175.0 # cm
test_weight = 72.0  # kg

# Linear Regression inference
pred_weight = reg_model.predict([[test_height]])[0]
print(f"Input: Height = {test_height} cm, Weight = {test_weight} kg")
print(f"-> Linear Regression Predicted Population Weight: {pred_weight:.1f} kg")

# Logistic Regression inference
prob = clf_model.predict_proba([[test_height, test_weight]])[0]
pred_gender_idx = clf_model.predict([[test_height, test_weight]])[0]
gender_name = "Female" if pred_gender_idx == 1 else "Male"

print(f"-> Logistic Regression Prediction: {gender_name}")
print(f"   Probability: Male={prob[0]*100:.1f}%, Female={prob[1]*100:.1f}%")

print("\n" + "="*70)
print("ALL DONE! Files generated:")
print(" - weight_height_linear.pkl")
print(" - gender_classification.pkl")
print(" - health_tracker_model_params.json")
print("="*70)

# In Google Colab, you can download all files at once:
# from google.colab import files
# files.download('weight_height_linear.pkl')
# files.download('gender_classification.pkl')
# files.download('health_tracker_model_params.json')
