import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier

# ======================
# Load your dataset
# ======================
# Replace with your actual dataset
data = pd.read_csv(r"C:\Users\Aravind\Desktop\liver disease\Liver_data.csv")

X = data.drop("target", axis=1)   # features
y = data["target"]                # labels (0 = no disorder, 1 = disorder)

# ======================
# Train/Test Split
# ======================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ======================
# Scale Features
# ======================
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# ======================
# Models
# ======================
models = {
    "Logistic Regression": LogisticRegression(class_weight="balanced", max_iter=500, random_state=42),
    "SVM": SVC(kernel="rbf", class_weight="balanced", probability=True, random_state=42),
    "Neural Network (MLP)": MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=1000, random_state=42)
}

# ======================
# Training & Evaluation
# ======================
results = []

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    results.append([name, acc, prec, rec, f1])

# ======================
# Results Table
# ======================
results_df = pd.DataFrame(results, columns=["Model", "Accuracy", "Precision", "Recall", "F1 Score"])
print("\n=== Model Performance ===")
print(results_df)

# ======================
# Detailed Report for Best Model
# ======================
best_model_name = results_df.sort_values(by="F1 Score", ascending=False).iloc[0]["Model"]
print(f"\nDetailed Classification Report for {best_model_name}:")
print(classification_report(y_test, models[best_model_name].predict(X_test)))
