import pickle
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score

# ==== Prepare Columns ====
columns = ['Age', 'Gender', 'Total_Bilirubin', 'Alkaline_Phosphotase',
           'Alamine_Aminotransferase', 'Aspartate_Aminotransferase',
           'Total_Protiens', 'Albumin', 'Albumin_and_Globulin_Ratio']

# ==== Example User Data (can be replaced with input) ====
# Uncomment below to take input from user:
"""
age = int(input("Age (in years): "))
gender_input = input("Gender (Male/Female): ").strip().lower()
if gender_input == "male":
    gender = 1
elif gender_input == "female":
    gender = 0
else:
    print("Invalid gender. Please enter 'Male' or 'Female'.")
    exit()

tb = float(input("Total Bilirubin: "))
alp = int(input("Alkaline Phosphotase: "))
alt = int(input("Alamine Aminotransferase: "))
ast = int(input("Aspartate Aminotransferase: "))
tp = float(input("Total Proteins: "))
alb = float(input("Albumin: "))
agr = float(input("Albumin and Globulin Ratio: "))

user_data = pd.DataFrame([[age, gender, tb, alp, alt, ast, tp, alb, agr]], columns=columns)
"""
# Test input
user_data = pd.DataFrame([[65, 1, 0.7, 187, 16.6, 1.3, 4.5, 1.2, 1.1]], columns=columns)

# ==== Load Dataset for Metrics ====
dataset = pd.read_csv(r"C:\Users\Aravind\Desktop\liver disease\Liver_data.csv")
dataset['Albumin_and_Globulin_Ratio'] = dataset['Albumin_and_Globulin_Ratio'].fillna(
    dataset['Albumin_and_Globulin_Ratio'].median()
)
dataset['Gender'] = np.where(dataset['Gender'] == 'Male', 1, 0)
dataset = dataset.drop('Direct_Bilirubin', axis=1)

X = dataset.iloc[:, :-1]
y = dataset.iloc[:, -1]
y = y.replace({1: 0, 2: 1})

# Match training script: No balancing here for direct performance check
X_train, y_train = X.iloc[:400], y.iloc[:400]
X_test, y_test = X.iloc[400:], y.iloc[400:]

# ==== Model Paths ====
model_paths = {
    "XGBoost": r"C:\Users\Aravind\Desktop\liver disease\XGBoost_model.pkl",
    "LightGBM": r"C:\Users\Aravind\Desktop\liver disease\LightGBM_model.pkl",
    "CatBoost": r"C:\Users\Aravind\Desktop\liver disease\CatBoost_model.pkl",
    "RandomForest": r"C:\Users\Aravind\Desktop\liver disease\RandomForest_model.pkl"
}

# ==== Predictions & Metrics ====
print("\nPrediction & Performance Results:")
for model_name, model_path in model_paths.items():
    model = pickle.load(open(model_path, 'rb'))
    
    # Prediction for given user data
    prediction = model.predict(user_data)
    result = "🔴 Liver Disorder Detected" if prediction[0] == 1 else "🟢 No Liver Disorder"
    
    # Performance on test set
    y_pred_test = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred_test)
    prec = precision_score(y_test, y_pred_test, zero_division=0)
    rec = recall_score(y_test, y_pred_test, zero_division=0)
    
    print(f"\n{model_name} Prediction: {result}")
    print(f"{model_name} Accuracy: {acc:.4f}")
    print(f"{model_name} Precision: {prec:.4f}")
    print(f"{model_name} Recall: {rec:.4f}")
