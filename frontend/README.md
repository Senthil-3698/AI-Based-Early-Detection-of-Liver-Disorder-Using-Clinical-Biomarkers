# Intelligent Liver Disease Prediction Suite - Frontend

## 🚀 Features

- **Interactive Web Interface** - Modern, responsive UI with medical theme
- **7 AI Models** - Compare predictions across multiple algorithms
- **Real-time Predictions** - Instant liver disease diagnosis
- **99.74% Accuracy** - Powered by Random Forest classifier
- **Visual Dashboards** - Beautiful comparison charts and metrics
- **Sample Data** - Quick testing with pre-filled patient data

## 📋 Prerequisites

- Python 3.8+
- Trained ML models (in `../liver disease/` directory)
- Modern web browser

## 🔧 Installation

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Ensure models are available:**
Make sure the following model files exist in `../liver disease/`:
- RandomForest_model.pkl
- XGBoost_model.pkl
- CatBoost_model.pkl
- LightGBM_model.pkl
- LogisticRegression_model.pkl
- SVM_model.pkl
- MLP_model.pkl

## 🎯 Running the Application

1. **Start the Flask server:**
```bash
python app.py
```

2. **Open your browser:**
Navigate to: `http://localhost:5000`

3. **Use the application:**
   - Enter patient clinical biomarkers
   - Select AI model
   - Click "Predict" for diagnosis
   - Or use "Compare All Models" to see predictions from all 7 models

## 📁 Project Structure

```
frontend/
├── app.py                      # Flask backend API
├── requirements.txt            # Python dependencies
├── templates/
│   └── index.html             # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css          # Interactive CSS styling
│   └── js/
│       └── script.js          # Frontend JavaScript logic
└── README.md                   # This file
```

## 🎨 Features Breakdown

### Home Section
- Project overview with key metrics
- Model performance comparison table
- 99.74% accuracy highlight

### Prediction Section
- Patient demographics input
- Liver function test parameters
- Enzyme level measurements
- Real-time AI-powered diagnosis
- Confidence scores and risk levels

### Model Comparison
- Side-by-side comparison of all 7 models
- Accuracy and confidence metrics
- Visual diagnosis cards

### About Section
- Project methodology
- Dataset information
- Clinical biomarkers used
- AI model details

## 🔬 Clinical Biomarkers Used

1. Age
2. Gender
3. Total Bilirubin
4. Alkaline Phosphatase
5. Alanine Aminotransferase (ALT)
6. Aspartate Aminotransferase (AST)
7. Total Proteins
8. Albumin
9. Albumin/Globulin Ratio

## 🤖 AI Models

| Model | Accuracy | Precision | Use Case |
|-------|----------|-----------|----------|
| Random Forest | 99.74% | 99.49% | **Best Overall** |
| XGBoost | 99.64% | 99.20% | High Performance |
| CatBoost | 99.48% | 99.14% | Categorical Features |
| LightGBM | 99.46% | 98.92% | Fast Training |
| MLP | 76.33% | 58.03% | Neural Network |
| Logistic Regression | 63.61% | 42.84% | Baseline |
| SVM | 58.92% | 39.93% | Support Vector |

## 🎨 UI Highlights

- **Medical Theme** - Professional healthcare color scheme
- **Animated Background** - Subtle medical cross animations
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Interactive Elements** - Hover effects, transitions, smooth scrolling
- **Loading States** - Beautiful loading animations
- **Real-time Validation** - Form validation with helpful messages

## ⚙️ API Endpoints

### POST /predict
Predict liver disease for a single patient using selected model.

**Request:**
```json
{
  "age": 45,
  "gender": "Male",
  "total_bilirubin": 0.7,
  "alkaline_phosphotase": 187,
  "alamine_aminotransferase": 16,
  "aspartate_aminotransferase": 18,
  "total_protiens": 6.8,
  "albumin": 3.3,
  "albumin_and_globulin_ratio": 0.9,
  "model": "RandomForest"
}
```

**Response:**
```json
{
  "prediction": 0,
  "diagnosis": "No Liver Disease",
  "confidence": 98.5,
  "model_used": "RandomForest",
  "model_accuracy": 99.74,
  "risk_level": "Low Risk"
}
```

### POST /compare
Compare predictions across all models.

**Response:**
```json
{
  "results": [
    {
      "model": "RandomForest",
      "prediction": 0,
      "diagnosis": "Healthy",
      "confidence": 98.5,
      "accuracy": 99.74
    },
    ...
  ]
}
```

### GET /api/performance
Get performance metrics for all models.

## 🔐 Security Notes

- Input validation on both frontend and backend
- Secure form handling
- Error handling for edge cases
- CORS protection (configure as needed)

## 📊 Sample Data

Click "Load Sample Data" button to fill the form with a healthy patient profile:
- Age: 45 years
- Gender: Male
- All biomarkers within normal ranges

## 🎯 Keyboard Shortcuts

- `Ctrl/Cmd + H` - Navigate to Home
- `Ctrl/Cmd + P` - Navigate to Predict
- `Ctrl/Cmd + C` - Navigate to Compare

## ⚠️ Disclaimer

This tool is designed for **research and educational purposes only**. Always consult qualified healthcare professionals for medical diagnosis and treatment decisions.

## 📝 License

This project is part of the Intelligent Liver Disease Prediction Suite.

## 🤝 Contributing

For improvements or bug reports, please contact the development team.

## 📧 Support

For technical support or questions, please refer to the project documentation.

---

**Powered by AI & Machine Learning** | © 2026 Intelligent Liver Disease Prediction Suite
