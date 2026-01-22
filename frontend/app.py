"""
Intelligent Liver Disease Prediction Suite - Backend API
Flask application for serving ML model predictions
"""

from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import pandas as pd
import os
from pathlib import Path

app = Flask(__name__)

# Model paths - Correct location
MODEL_DIR = Path(__file__).parent.parent / "liver disease"
MODELS = {
    "RandomForest": "RandomForest_model.pkl",
    "CatBoost": "CatBoost_model.pkl",
    "XGBoost": "XGBoost_model.pkl",
    "LightGBM": "LightGBM_model.pkl",
    "LogisticRegression": "LogisticRegression_model.pkl",
    "SVM": "SVM_model.pkl",
    "MLP": "MLP_model.pkl"
}

# Load all models
loaded_models = {}
for model_name, model_file in MODELS.items():
    try:
        model_path = MODEL_DIR / model_file
        with open(model_path, 'rb') as f:
            loaded_models[model_name] = pickle.load(f)
        print(f"✅ Loaded {model_name}")
    except Exception as e:
        print(f"❌ Error loading {model_name}: {e}")

# Feature names (based on the dataset, excluding Direct_Bilirubin)
FEATURE_NAMES = [
    'Age', 'Gender', 'Total_Bilirubin', 'Alkaline_Phosphotase',
    'Alamine_Aminotransferase', 'Aspartate_Aminotransferase',
    'Total_Protiens', 'Albumin', 'Albumin_and_Globulin_Ratio'
]

# Model performance metrics
MODEL_PERFORMANCE = {
    "RandomForest": {"accuracy": 99.74, "precision": 99.49, "recall": 99.60, "f1": 99.54, "auc": 99.99},
    "CatBoost": {"accuracy": 99.48, "precision": 99.14, "recall": 99.03, "f1": 99.09, "auc": 99.98},
    "XGBoost": {"accuracy": 99.64, "precision": 99.20, "recall": 99.54, "f1": 99.37, "auc": 99.95},
    "LightGBM": {"accuracy": 99.46, "precision": 98.92, "recall": 99.20, "f1": 99.06, "auc": 99.96},
    "MLP": {"accuracy": 76.33, "precision": 58.03, "recall": 62.17, "f1": 60.03, "auc": 84.13},
    "LogisticRegression": {"accuracy": 63.61, "precision": 42.84, "recall": 81.65, "f1": 56.20, "auc": 74.76},
    "SVM": {"accuracy": 58.92, "precision": 39.93, "recall": 86.61, "f1": 54.66, "auc": 75.26}
}

@app.route('/')
def home():
    """Render the main page"""
    return render_template('index.html', models=MODELS.keys(), performance=MODEL_PERFORMANCE)

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests"""
    try:
        data = request.get_json()
        
        # Extract features
        features = [
            float(data['age']),
            1 if data['gender'].lower() == 'male' else 0,
            float(data['total_bilirubin']),
            float(data['alkaline_phosphotase']),
            float(data['alamine_aminotransferase']),
            float(data['aspartate_aminotransferase']),
            float(data['total_protiens']),
            float(data['albumin']),
            float(data['albumin_and_globulin_ratio'])
        ]
        
        # Get selected model
        model_name = data.get('model', 'RandomForest')
        
        if model_name not in loaded_models:
            return jsonify({'error': f'Model {model_name} not available'}), 400
        
        # Make prediction
        model = loaded_models[model_name]
        input_data = np.array([features])
        prediction = model.predict(input_data)[0]
        
        # Get probability if available
        try:
            probability = model.predict_proba(input_data)[0]
            confidence = float(max(probability)) * 100
        except:
            confidence = None
        
        # Prepare response
        result = {
            'prediction': int(prediction),
            'diagnosis': 'Liver Disease Detected' if prediction == 1 else 'No Liver Disease',
            'confidence': confidence,
            'model_used': model_name,
            'model_accuracy': MODEL_PERFORMANCE[model_name]['accuracy'],
            'risk_level': get_risk_level(prediction, confidence)
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/compare', methods=['POST'])
def compare_models():
    """Compare predictions across all models"""
    try:
        data = request.get_json()
        
        # Extract features
        features = [
            float(data['age']),
            1 if data['gender'].lower() == 'male' else 0,
            float(data['total_bilirubin']),
            float(data['alkaline_phosphotase']),
            float(data['alamine_aminotransferase']),
            float(data['aspartate_aminotransferase']),
            float(data['total_protiens']),
            float(data['albumin']),
            float(data['albumin_and_globulin_ratio'])
        ]
        
        input_data = np.array([features])
        results = []
        
        # Get predictions from all models
        for model_name, model in loaded_models.items():
            try:
                prediction = model.predict(input_data)[0]
                try:
                    probability = model.predict_proba(input_data)[0]
                    confidence = float(max(probability)) * 100
                except:
                    confidence = None
                
                results.append({
                    'model': model_name,
                    'prediction': int(prediction),
                    'diagnosis': 'Liver Disease' if prediction == 1 else 'Healthy',
                    'confidence': confidence,
                    'accuracy': MODEL_PERFORMANCE[model_name]['accuracy']
                })
            except Exception as e:
                print(f"Error with {model_name}: {e}")
        
        return jsonify({'results': results})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/performance')
def get_performance():
    """Get model performance metrics"""
    return jsonify(MODEL_PERFORMANCE)

def get_risk_level(prediction, confidence):
    """Determine risk level based on prediction and confidence"""
    if prediction == 0:
        return 'Low Risk'
    elif confidence and confidence > 90:
        return 'High Risk'
    elif confidence and confidence > 70:
        return 'Moderate Risk'
    else:
        return 'Uncertain'

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🏥 Intelligent Liver Disease Prediction Suite")
    print("="*60)
    print(f"✅ Loaded {len(loaded_models)} ML models")
    print("🌐 Starting Flask server...")
    print("="*60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
