import pickle
import pandas as pd

# Load trained model
model = pickle.load(open(r'C:\Users\senth\OneDrive\Desktop\Liver Disease\Liver2.pkl', 'rb'))

# Feature names as used during training (including typo!)
columns = ['Age', 'Gender', 'Total_Bilirubin', 'Alkaline_Phosphotase',
           'Alamine_Aminotransferase', 'Aspartate_Aminotransferase',
           'Total_Protiens', 'Albumin', 'Albumin_and_Globulin_Ratio']

print("\n Please enter the following values:")

# Get user inputs
age = int(input("Age (in years): "))
gender_input = input("Gender (Male/Female): ").strip().lower()

# Gender encoding
if gender_input == "male":
    gender = 1
elif gender_input == "female":
    gender = 0
else:
    print("Invalid gender. Please enter 'Male' or 'Female'.")
    exit()

tb = float(input("Total Bilirubin (e.g., 1.2): "))
alp = int(input("Alkaline Phosphotase (e.g., 210): "))
alt = int(input("Alamine Aminotransferase (e.g., 30): "))
ast = int(input("Aspartate Aminotransferase (e.g., 70): "))
tp = float(input("Total Proteins (e.g., 6.8): "))
alb = float(input("Albumin (e.g., 3.1): "))
agr = float(input("Albumin and Globulin Ratio (e.g., 1.0): "))

# Create input DataFrame
user_data = pd.DataFrame([[age, gender, tb, alp, alt, ast, tp, alb, agr]], columns=columns)

# Predict
prediction = model.predict(user_data)

# Output result
print("\n Prediction Result:")
if prediction[0] == 1:
    print("The person is likely to have liver disease.")
else:
    print("The person is likely healthy (no liver disease). Yayyy!")
