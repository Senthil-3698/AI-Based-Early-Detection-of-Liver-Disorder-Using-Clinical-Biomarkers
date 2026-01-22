# Importing Libraries
import pandas as pd
import numpy as np
import pickle
from imblearn.combine import SMOTETomek
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Display all columns
pd.set_option('display.max_columns', None)

# Reading Dataset
dataset = pd.read_csv(r"C:\Users\senth\OneDrive\Desktop\Liver Disease\Liver_data.csv")

# Fill NaN in 'Albumin_and_Globulin_Ratio' with median
dataset['Albumin_and_Globulin_Ratio'] = dataset['Albumin_and_Globulin_Ratio'].fillna(dataset['Albumin_and_Globulin_Ratio'].median())

# Label Encoding for Gender
dataset['Gender'] = np.where(dataset['Gender'] == 'Male', 1, 0)

# Drop 'Direct_Bilirubin'
dataset = dataset.drop('Direct_Bilirubin', axis=1)

# Features and Target
X = dataset.iloc[:, :-1]
y = dataset.iloc[:, -1]

# Apply SMOTE + Tomek
smote = SMOTETomek()
X_smote, y_smote = smote.fit_resample(X, y)

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X_smote, y_smote, test_size=0.3, random_state=33)

# Train RandomForest Classifier
RandomForest = RandomForestClassifier()
RandomForest.fit(X_train, y_train)

# Save model using full path
filename = r'C:\Users\senth\OneDrive\Desktop\Liver Disease\Liver2.pkl'
pickle.dump(RandomForest, open(filename, 'wb'))
