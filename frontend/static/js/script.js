// ==================== NAVIGATION & SECTION MANAGEMENT ====================
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    initializeForms();
    attachEventListeners();
});

function initializeNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const sectionId = this.getAttribute('data-section');
            navigateToSection(sectionId);
        });
    });
}

function navigateToSection(sectionId) {
    // Update navigation active state
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    document.querySelector(`[data-section="${sectionId}"]`).classList.add('active');
    
    // Update section visibility
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(sectionId).classList.add('active');
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ==================== FORM INITIALIZATION ====================
function initializeForms() {
    const predictionForm = document.getElementById('predictionForm');
    
    if (predictionForm) {
        predictionForm.addEventListener('submit', handlePrediction);
    }
}

function attachEventListeners() {
    // Add input validation listeners
    const numericInputs = document.querySelectorAll('input[type="number"]');
    numericInputs.forEach(input => {
        input.addEventListener('input', function() {
            validateNumericInput(this);
        });
    });
}

function validateNumericInput(input) {
    const value = parseFloat(input.value);
    const min = parseFloat(input.min);
    const max = parseFloat(input.max);
    
    if (min !== undefined && value < min) {
        input.setCustomValidity(`Value must be at least ${min}`);
    } else if (max !== undefined && value > max) {
        input.setCustomValidity(`Value must be at most ${max}`);
    } else {
        input.setCustomValidity('');
    }
}

// ==================== PREDICTION HANDLING ====================
async function handlePrediction(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = {
        age: formData.get('age'),
        gender: formData.get('gender'),
        total_bilirubin: formData.get('total_bilirubin'),
        alkaline_phosphotase: formData.get('alkaline_phosphotase'),
        alamine_aminotransferase: formData.get('alamine_aminotransferase'),
        aspartate_aminotransferase: formData.get('aspartate_aminotransferase'),
        total_protiens: formData.get('total_protiens'),
        albumin: formData.get('albumin'),
        albumin_and_globulin_ratio: formData.get('albumin_and_globulin_ratio'),
        model: formData.get('model')
    };
    
    showLoading();
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displayPredictionResult(result);
        } else {
            showError(result.error || 'Prediction failed');
        }
    } catch (error) {
        showError('Network error. Please try again.');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

function displayPredictionResult(result) {
    const resultsContainer = document.getElementById('resultsContainer');
    const predictionResult = document.getElementById('predictionResult');
    
    const isPositive = result.prediction === 1;
    const icon = isPositive ? 'fa-exclamation-triangle' : 'fa-check-circle';
    const badgeClass = isPositive ? 'positive' : 'negative';
    
    const confidenceText = result.confidence 
        ? `Confidence: ${result.confidence.toFixed(2)}%`
        : 'Confidence: N/A';
    
    // Calculate health score (inverse of risk for positive cases)
    const healthScore = isPositive ? (100 - result.confidence) : result.confidence;
    const healthPercentage = healthScore ? healthScore.toFixed(0) : 50;
    
    predictionResult.innerHTML = `
        <div class="result-badge ${badgeClass}">
            <div class="result-icon">
                <i class="fas ${icon}"></i>
            </div>
            <div class="result-label">${result.diagnosis}</div>
            <div class="result-confidence">${confidenceText}</div>
            <div class="result-confidence">Risk Level: ${result.risk_level}</div>
            
            <!-- Health Meter -->
            <div class="health-meter">
                <div class="health-meter-label">Liver Health Score</div>
                <div class="health-meter-bar">
                    <div class="health-meter-fill ${badgeClass}" style="width: ${healthPercentage}%">
                        <span class="health-meter-value">${healthPercentage}%</span>
                    </div>
                </div>
                <div class="health-meter-scale">
                    <span>Critical</span>
                    <span>Moderate</span>
                    <span>Healthy</span>
                </div>
            </div>
        </div>
    `;
    
    document.getElementById('modelUsed').textContent = result.model_used;
    document.getElementById('modelAccuracy').textContent = `${result.model_accuracy}%`;
    
    resultsContainer.style.display = 'block';
    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// ==================== MODEL COMPARISON ====================
async function compareModels() {
    const form = document.getElementById('predictionForm');
    
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    const formData = new FormData(form);
    const data = {
        age: formData.get('age'),
        gender: formData.get('gender'),
        total_bilirubin: formData.get('total_bilirubin'),
        alkaline_phosphotase: formData.get('alkaline_phosphotase'),
        alamine_aminotransferase: formData.get('alamine_aminotransferase'),
        aspartate_aminotransferase: formData.get('aspartate_aminotransferase'),
        total_protiens: formData.get('total_protiens'),
        albumin: formData.get('albumin'),
        albumin_and_globulin_ratio: formData.get('albumin_and_globulin_ratio')
    };
    
    showLoading();
    
    try {
        const response = await fetch('/compare', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displayComparisonResults(result.results);
        } else {
            showError(result.error || 'Comparison failed');
        }
    } catch (error) {
        showError('Network error. Please try again.');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

function displayComparisonResults(results) {
    const comparisonResults = document.getElementById('comparisonResults');
    
    let html = '';
    results.forEach(result => {
        const isPositive = result.prediction === 1;
        const icon = isPositive ? 'fa-exclamation-triangle' : 'fa-check-circle';
        const resultClass = isPositive ? 'positive' : 'negative';
        const confidenceText = result.confidence 
            ? `${result.confidence.toFixed(2)}% confidence`
            : 'N/A';
        
        html += `
            <div class="comparison-card">
                <div class="comparison-header">
                    <span class="model-name">${result.model}</span>
                    <span class="accuracy-badge">${result.accuracy}%</span>
                </div>
                <div class="comparison-result ${resultClass}">
                    <i class="fas ${icon}"></i>
                    <div class="comparison-diagnosis">${result.diagnosis}</div>
                    <div class="comparison-confidence">${confidenceText}</div>
                </div>
            </div>
        `;
    });
    
    comparisonResults.innerHTML = html;
    comparisonResults.style.display = 'grid';
    comparisonResults.scrollIntoView({ behavior: 'smooth' });
}

// ==================== SAMPLE DATA ====================
function fillSampleData() {
    // Sample patient data (healthy profile)
    const sampleData = {
        age: 45,
        gender: 'Male',
        total_bilirubin: 0.7,
        alkaline_phosphotase: 187,
        alamine_aminotransferase: 16,
        aspartate_aminotransferase: 18,
        total_protiens: 6.8,
        albumin: 3.3,
        albumin_and_globulin_ratio: 0.9
    };
    
    // Fill form fields
    Object.keys(sampleData).forEach(key => {
        const input = document.querySelector(`[name="${key}"]`);
        if (input) {
            input.value = sampleData[key];
        }
    });
    
    showNotification('Sample data loaded successfully!', 'success');
}

// ==================== UI HELPERS ====================
function showLoading() {
    const overlay = document.getElementById('loadingOverlay');
    overlay.classList.add('active');
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    overlay.classList.remove('active');
}

function showError(message) {
    showNotification(message, 'error');
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'error' ? '#ef4444' : type === 'success' ? '#22c55e' : '#3b82f6'};
        color: white;
        border-radius: 0.5rem;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
        z-index: 10000;
        animation: slideIn 0.3s ease;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        max-width: 400px;
    `;
    
    const icon = type === 'error' ? 'fa-times-circle' : 
                 type === 'success' ? 'fa-check-circle' : 
                 'fa-info-circle';
    
    notification.innerHTML = `
        <i class="fas ${icon}"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 5000);
}

// Add notification animations to document
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(100%);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideOut {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }
`;
document.head.appendChild(style);

// ==================== FORM VALIDATION HELPERS ====================
function validateForm(formData) {
    const errors = [];
    
    // Age validation
    const age = parseFloat(formData.get('age'));
    if (age < 1 || age > 120) {
        errors.push('Age must be between 1 and 120');
    }
    
    // Numeric validations
    const numericFields = [
        'total_bilirubin',
        'alkaline_phosphotase',
        'alamine_aminotransferase',
        'aspartate_aminotransferase',
        'total_protiens',
        'albumin',
        'albumin_and_globulin_ratio'
    ];
    
    numericFields.forEach(field => {
        const value = parseFloat(formData.get(field));
        if (isNaN(value) || value < 0) {
            errors.push(`${field.replace(/_/g, ' ')} must be a positive number`);
        }
    });
    
    return errors;
}

// ==================== KEYBOARD SHORTCUTS ====================
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + H = Home
    if ((e.ctrlKey || e.metaKey) && e.key === 'h') {
        e.preventDefault();
        navigateToSection('home');
    }
    
    // Ctrl/Cmd + P = Predict
    if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
        e.preventDefault();
        navigateToSection('predict');
    }
    
    // Ctrl/Cmd + C = Compare
    if ((e.ctrlKey || e.metaKey) && e.key === 'c') {
        e.preventDefault();
        navigateToSection('compare');
    }
});

// ==================== SMOOTH SCROLL ====================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ==================== EXPORT FUNCTIONS ====================
window.navigateToSection = navigateToSection;
window.compareModels = compareModels;
window.fillSampleData = fillSampleData;
