# ===================== Import Libraries =====================
import pandas as pd
import numpy as np
import pickle
import time
from sklearn.model_selection import train_test_split
from imblearn.combine import SMOTETomek
from sklearn.metrics import accuracy_score

# Models
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier

# ===================== Load Dataset =====================
dataset = pd.read_csv(r"C:\Users\Aravind\Desktop\liver disease\Liver_data.csv", encoding='cp1252')

# Encode Gender: Male=1, Female=0
dataset['Gender'] = np.where(dataset['Gender'] == 'Male', 1, 0)

# Drop redundant column if exists
if 'Direct_Bilirubin' in dataset.columns:
    dataset = dataset.drop('Direct_Bilirubin', axis=1)

# Features and Target
X = dataset.iloc[:, :-1]
y = dataset.iloc[:, -1]
y = y.replace({1: 0, 2: 1})  # remap target

# ===================== Split Dataset =====================
# First split into train+test (test is unseen and saved for later evaluation)
X_train_full, X_test, y_train_full, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Save test set for evaluation script
test_data = pd.concat([X_test, y_test], axis=1)
test_data.to_csv(r"C:\Users\Aravind\Desktop\liver disease\test_data.csv", index=False)

# Now split train_full into train+validation
X_train, X_val, y_train, y_val = train_test_split(
    X_train_full, y_train_full, test_size=0.2, stratify=y_train_full, random_state=42
)

# ===================== Check & Handle Missing Values =====================
print("\n🔍 Checking for missing values...")
missing = X_train.isnull().sum()
missing = missing[missing > 0]
if not missing.empty:
    print("\nColumns with missing values:")
    print(missing)
    print("\n➡️ Filling missing values with median/mode...")
else:
    print("✅ No missing values found.")

# Fill numeric missing values
X_train = X_train.fillna(X_train.median())
X_val = X_val.fillna(X_val.median())
X_test = X_test.fillna(X_test.median())

# Fill categorical (if any)
if 'Gender' in X_train.columns:
    mode_gender = X_train['Gender'].mode()[0]
    X_train['Gender'] = X_train['Gender'].fillna(mode_gender)
    X_val['Gender'] = X_val['Gender'].fillna(mode_gender)
    X_test['Gender'] = X_test['Gender'].fillna(mode_gender)

# ===================== Handle Class Imbalance =====================
print("\n⚖️ Applying SMOTETomek to handle imbalance...")
smt = SMOTETomek(random_state=42)
X_train_res, y_train_res = smt.fit_resample(X_train, y_train)
print(f"✅ Resampling complete. Class distribution after SMOTETomek:\n{y_train_res.value_counts()}")

# ===================== Define Models =====================
models = {
    "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42),
    "LightGBM": LGBMClassifier(random_state=42),
    "CatBoost": CatBoostClassifier(verbose=0, random_state=42),
    "RandomForest": RandomForestClassifier(random_state=42),
    "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
    "SVM": SVC(probability=True, random_state=42),
    "MLP": MLPClassifier(max_iter=1000, random_state=42)
}

save_path = r"C:\Users\Aravind\Desktop\liver disease"

# ===================== Train, Validate and Save Models =====================
print("\n🚀 Starting training process...")
for name, model in models.items():
    print(f"\nTraining {name} ...")
    start = time.time()
    model.fit(X_train_res, y_train_res)
    end = time.time()

    # Validation accuracy
    val_pred = model.predict(X_val)
    acc = accuracy_score(y_val, val_pred)
    print(f"{name} Validation Accuracy: {acc:.4f}")
    print(f"⏱️ Training time: {end - start:.2f} seconds")

    # Save model
    pickle.dump(model, open(f"{save_path}\\{name}_model.pkl", "wb"))

print("\n✅ Training complete. All models saved successfully!")
print("✅ Test set saved for evaluation at: test_data.csv")
