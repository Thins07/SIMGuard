/**
 * SIMGuard ML Dashboard - JavaScript
 * Handles form submission, API calls, and UI updates
 */

// API Configuration
const API_BASE_URL = 'http://localhost:5000';
const API_ENDPOINTS = {
    predict: `${API_BASE_URL}/predict`,
    health: `${API_BASE_URL}/`
};

// DOM Elements
const detectionForm = document.getElementById('detectionForm');
const clearBtn = document.getElementById('clearBtn');
const exportBtn = document.getElementById('exportBtn');
const emptyState = document.getElementById('emptyState');
const loadingState = document.getElementById('loadingState');
const resultsDisplay = document.getElementById('resultsDisplay');
const riskIndicator = document.getElementById('riskIndicator');
const riskIcon = document.getElementById('riskIcon');
const riskStatus = document.getElementById('riskStatus');
const riskMessage = document.getElementById('riskMessage');
const confidenceFill = document.getElementById('confidenceFill');
const confidenceText = document.getElementById('confidenceText');
const riskFactorsList = document.getElementById('riskFactorsList');
const predictionsBody = document.getElementById('predictionsBody');

// State Management
let currentPrediction = null;
let predictionHistory = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadPredictionHistory();
    updatePredictionsTable();
    
    // Event Listeners
    detectionForm.addEventListener('submit', handleFormSubmit);
    clearBtn.addEventListener('click', handleClearForm);
    exportBtn.addEventListener('click', handleExportReport);
});

/**
 * Handle form submission
 */
async function handleFormSubmit(e) {
    e.preventDefault();
    
    // Show loading state
    showLoadingState();
    
    try {
        // Collect form data
        const formData = collectFormData();
        
        // Make API call
        const response = await fetch(API_ENDPOINTS.predict, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }
        
        const result = await response.json();
        
        // Store current prediction
        currentPrediction = {
            ...result,
            timestamp: new Date().toISOString(),
            formData: formData
        };
        
        // Add to history
        addToPredictionHistory(currentPrediction);
        
        // Display results
        displayResults(result);
        
    } catch (error) {
        console.error('Prediction error:', error);
        showError(error.message);
    }
}

/**
 * Collect form data into object
 */
function collectFormData() {
    const formData = new FormData(detectionForm);
    const data = {};
    
    // Numeric fields
    data.distance_change = parseFloat(formData.get('distance_change')) || 0;
    data.time_since_sim_change = parseFloat(formData.get('time_since_sim_change')) || 0;
    data.num_failed_logins_last_24h = parseInt(formData.get('num_failed_logins_last_24h')) || 0;
    data.num_calls_last_24h = parseInt(formData.get('num_calls_last_24h')) || 0;
    data.num_sms_last_24h = parseInt(formData.get('num_sms_last_24h')) || 0;
    data.data_usage_change_percent = parseFloat(formData.get('data_usage_change_percent')) || 0;
    data.change_in_cell_tower_id = parseInt(formData.get('change_in_cell_tower_id')) || 0;
    
    // Boolean fields (checkboxes)
    data.is_roaming = document.getElementById('isRoaming').checked ? 1 : 0;
    data.sim_change_flag = document.getElementById('simChange').checked ? 1 : 0;
    data.device_change_flag = document.getElementById('deviceChange').checked ? 1 : 0;
    
    // Text fields
    data.current_city = formData.get('current_city') || '';
    data.previous_city = formData.get('previous_city') || '';
    
    return data;
}

/**
 * Display prediction results
 */
function displayResults(result) {
    // Hide loading, show results
    loadingState.classList.add('hidden');
    emptyState.classList.add('hidden');
    resultsDisplay.classList.remove('hidden');
    
    // Determine risk level
    const isSuspicious = result.prediction === 1;
    const confidence = result.confidence;
    
    // Update risk indicator
    riskIndicator.className = 'risk-indicator';
    riskIndicator.classList.add(isSuspicious ? 'suspicious' : 'safe');
    
    riskStatus.textContent = isSuspicious ? 'SUSPICIOUS 🚨' : 'SAFE ✅';
    riskMessage.textContent = isSuspicious 
        ? 'High probability of SIM swap attack detected'
        : 'No suspicious activity detected';
    
    // Update confidence score with animation
    setTimeout(() => {
        confidenceFill.style.width = `${confidence}%`;
        confidenceText.textContent = `${confidence.toFixed(1)}%`;
    }, 100);
    
    // Display risk factors
    displayRiskFactors(result.risk_factors || []);
    
    // Update predictions table
    updatePredictionsTable();
}

/**
 * Display risk factors
 */
function displayRiskFactors(factors) {
    riskFactorsList.innerHTML = '';

    if (factors.length === 0) {
        riskFactorsList.innerHTML = '<li>No significant risk factors identified</li>';
        return;
    }

    // Show top 3 factors
    factors.slice(0, 3).forEach(factor => {
        const li = document.createElement('li');
        li.textContent = factor;
        riskFactorsList.appendChild(li);
    });
}

/**
 * Show loading state
 */
function showLoadingState() {
    emptyState.classList.add('hidden');
    resultsDisplay.classList.add('hidden');
    loadingState.classList.remove('hidden');
}

/**
 * Show error message
 */
function showError(message) {
    loadingState.classList.add('hidden');
    emptyState.classList.remove('hidden');

    alert(`Error: ${message}\n\nPlease ensure the backend server is running on ${API_BASE_URL}`);
}

/**
 * Handle clear form button
 */
function handleClearForm() {
    detectionForm.reset();

    // Reset results display
    emptyState.classList.remove('hidden');
    loadingState.classList.add('hidden');
    resultsDisplay.classList.add('hidden');

    currentPrediction = null;
}

/**
 * Handle export report button
 */
function handleExportReport() {
    if (!currentPrediction) {
        alert('No prediction to export');
        return;
    }

    // Create report content
    const report = generateReport(currentPrediction);

    // Download as text file
    const blob = new Blob([report], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `simguard-report-${new Date().getTime()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

/**
 * Generate report text
 */
function generateReport(prediction) {
    const timestamp = new Date(prediction.timestamp).toLocaleString();
    const isSuspicious = prediction.prediction === 1;

    let report = `
╔═══════════════════════════════════════════════════════════╗
║           SIMGuard - Detection Report                     ║
╚═══════════════════════════════════════════════════════════╝

Report Generated: ${timestamp}

RISK ASSESSMENT
═══════════════════════════════════════════════════════════
Status: ${isSuspicious ? 'SUSPICIOUS 🚨' : 'SAFE ✅'}
Confidence: ${prediction.confidence.toFixed(2)}%
Prediction: ${isSuspicious ? 'SIM Swap Attack Detected' : 'No Attack Detected'}

RISK FACTORS
═══════════════════════════════════════════════════════════
`;

    if (prediction.risk_factors && prediction.risk_factors.length > 0) {
        prediction.risk_factors.forEach((factor, index) => {
            report += `${index + 1}. ${factor}\n`;
        });
    } else {
        report += 'No significant risk factors identified\n';
    }

    report += `
INPUT DATA
═══════════════════════════════════════════════════════════
Distance Change: ${prediction.formData.distance_change} km
Time Since SIM Change: ${prediction.formData.time_since_sim_change} hours
Failed Logins (24h): ${prediction.formData.num_failed_logins_last_24h}
Calls (24h): ${prediction.formData.num_calls_last_24h}
SMS (24h): ${prediction.formData.num_sms_last_24h}
Data Usage Change: ${prediction.formData.data_usage_change_percent}%
Cell Tower Changes: ${prediction.formData.change_in_cell_tower_id}
Is Roaming: ${prediction.formData.is_roaming ? 'Yes' : 'No'}
SIM Change Flag: ${prediction.formData.sim_change_flag ? 'Yes' : 'No'}
Device Change Flag: ${prediction.formData.device_change_flag ? 'Yes' : 'No'}
Current City: ${prediction.formData.current_city}
Previous City: ${prediction.formData.previous_city}

═══════════════════════════════════════════════════════════
SIMGuard - Final Year Project by Thinara | 2025
Powered by XGBoost ML Model
═══════════════════════════════════════════════════════════
`;

    return report;
}

/**
 * Add prediction to history
 */
function addToPredictionHistory(prediction) {
    predictionHistory.unshift(prediction);

    // Keep only last 5 predictions
    if (predictionHistory.length > 5) {
        predictionHistory = predictionHistory.slice(0, 5);
    }

    // Save to localStorage
    savePredictionHistory();
}

/**
 * Save prediction history to localStorage
 */
function savePredictionHistory() {
    try {
        localStorage.setItem('simguard_predictions', JSON.stringify(predictionHistory));
    } catch (error) {
        console.error('Error saving to localStorage:', error);
    }
}

/**
 * Load prediction history from localStorage
 */
function loadPredictionHistory() {
    try {
        const saved = localStorage.getItem('simguard_predictions');
        if (saved) {
            predictionHistory = JSON.parse(saved);
        }
    } catch (error) {
        console.error('Error loading from localStorage:', error);
        predictionHistory = [];
    }
}

/**
 * Update predictions table
 */
function updatePredictionsTable() {
    predictionsBody.innerHTML = '';

    if (predictionHistory.length === 0) {
        predictionsBody.innerHTML = `
            <tr class="empty-row">
                <td colspan="3">No predictions yet</td>
            </tr>
        `;
        return;
    }

    predictionHistory.forEach(prediction => {
        const row = document.createElement('tr');
        const timestamp = new Date(prediction.timestamp).toLocaleString();
        const isSuspicious = prediction.prediction === 1;
        const riskLevel = isSuspicious ? 'SUSPICIOUS' : 'SAFE';
        const badgeClass = isSuspicious ? 'suspicious' : 'safe';

        row.innerHTML = `
            <td>${timestamp}</td>
            <td><span class="risk-badge ${badgeClass}">${riskLevel}</span></td>
            <td>${prediction.confidence.toFixed(1)}%</td>
        `;

        predictionsBody.appendChild(row);
    });
}

/**
 * Clear prediction history
 */
function clearPredictionHistory() {
    if (confirm('Are you sure you want to clear all prediction history?')) {
        predictionHistory = [];
        savePredictionHistory();
        updatePredictionsTable();
    }
}

// Expose clear history function globally for potential UI button
window.clearPredictionHistory = clearPredictionHistory;
