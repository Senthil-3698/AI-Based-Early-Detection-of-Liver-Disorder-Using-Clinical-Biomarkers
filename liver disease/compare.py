# ===================== Import Libraries =====================
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, roc_curve
)
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

# ===================== Load & Clean Dataset =====================
dataset = pd.read_csv(r"C:\Users\Aravind\Desktop\liver disease\Liver_data.csv", encoding='cp1252')

# Handle missing values safely
for col in dataset.columns:
    if dataset[col].dtype in ['int64', 'float64']:
        dataset[col] = dataset[col].fillna(dataset[col].median())
    else:
        dataset[col] = dataset[col].fillna(dataset[col].mode()[0])

# Encode Gender
if 'Gender' in dataset.columns:
    dataset['Gender'] = np.where(dataset['Gender'] == 'Male', 1, 0)

# Drop Direct_Bilirubin if exists
if 'Direct_Bilirubin' in dataset.columns:
    dataset.drop('Direct_Bilirubin', axis=1, inplace=True)

# Split features and target
X = dataset.iloc[:, :-1]
y = dataset.iloc[:, -1].replace({1: 0, 2: 1})

# Handle missing again (for safety)
imputer = SimpleImputer(strategy='median')
X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)

# Split into train-test
X_train, X_test, y_train, y_test = train_test_split(
    X_imputed, y, test_size=0.2, stratify=y, random_state=42
)

# ===================== Model Filenames =====================
model_files = [
    "XGBoost_model.pkl",
    "LightGBM_model.pkl",
    "CatBoost_model.pkl",
    "RandomForest_model.pkl",
    "LogisticRegression_model.pkl",
    "SVM_model.pkl",
    "MLP_model.pkl"
]

save_path = r"C:\Users\Aravind\Desktop\liver disease"
results = []
roc_data = {}
conf_matrices = {}

# ===================== Evaluate Models =====================
for filename in model_files:
    model_path = f"{save_path}\\{filename}"
    model_name = filename.replace("_model.pkl", "")
    print(f"\nLoading {model_name}...")

    model = pickle.load(open(model_path, "rb"))

    # Predict
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)

    try:
        y_proba = model.predict_proba(X_test)[:, 1]
        auc = roc_auc_score(y_test, y_proba)
        fpr, tpr, _ = roc_curve(y_test, y_proba)
        roc_data[model_name] = (fpr, tpr, auc)
    except:
        auc = np.nan

    conf_matrices[model_name] = confusion_matrix(y_test, y_pred)
    results.append([model_name, acc, prec, rec, f1, auc])

# ===================== Summary Table =====================
results_df = pd.DataFrame(results, columns=["Model", "Accuracy", "Precision", "Recall", "F1 Score", "ROC-AUC"])
print("\n=========== Model Performance Summary ===========")
print(results_df)

# ===================== Visualization =====================
sns.set(style="whitegrid", font_scale=1.1)
fig, axes = plt.subplots(2, 3, figsize=(20, 12))
fig.suptitle("AI Model Performance Comparison", fontsize=20, fontweight="bold")

# ---------- 1️⃣ Bar Chart for Metrics ----------
ax = axes[0, 0]
metrics = ["Accuracy", "Precision", "Recall", "F1 Score", "ROC-AUC"]
results_melt = results_df.melt(id_vars="Model", value_vars=metrics, var_name="Metric", value_name="Score")
sns.barplot(x="Model", y="Score", hue="Metric", data=results_melt, ax=ax)
ax.set_title("Performance Metrics Comparison")
ax.tick_params(axis='x', rotation=45)
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

# ---------- 2️⃣ Radar Chart ----------
ax_radar = axes[0, 1]  # use next available subplot
angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False).tolist()
angles += angles[:1]
ax_radar = plt.subplot(2, 3, 2, polar=True)
for i, row in results_df.iterrows():
    values = row[metrics].tolist()
    values += values[:1]
    ax_radar.plot(angles, values, label=row["Model"])
    ax_radar.fill(angles, values, alpha=0.1)
ax_radar.set_xticks(angles[:-1])
ax_radar.set_xticklabels(metrics)
ax_radar.set_title("Radar Chart of Model Metrics")
ax_radar.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

# ---------- 3️⃣ ROC Curves ----------
ax = axes[0, 2]
for model_name, (fpr, tpr, auc) in roc_data.items():
    ax.plot(fpr, tpr, label=f"{model_name} (AUC={auc:.2f})")
ax.plot([0, 1], [0, 1], 'k--')
ax.set_title("ROC Curves")
ax.set_xlabel("False Positive Rate")
ax.set_ylabel("True Positive Rate")
ax.legend()

# Leave bottom row empty (future space)
for ax in axes[1]:
    ax.axis("off")

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

# ===================== Confusion Matrices for ALL Models =====================
fig_rows, fig_cols = 3, 3  # enough for 7 models
fig_cm, axes_cm = plt.subplots(fig_rows, fig_cols, figsize=(18, 14))
axes_cm = axes_cm.flatten()

fig_cm.suptitle("Confusion Matrices of All Models", fontsize=20, fontweight="bold")

for i, (model_name, cm) in enumerate(conf_matrices.items()):
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=axes_cm[i])
    axes_cm[i].set_title(f"{model_name}", fontsize=12, fontweight="bold")
    axes_cm[i].set_xlabel("Predicted")
    axes_cm[i].set_ylabel("Actual")

# Hide unused subplots
for j in range(i + 1, len(axes_cm)):
    fig_cm.delaxes(axes_cm[j])

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
