/* ============================================================================
   SRI LANKAN ML DASHBOARD - JAVASCRIPT
   File Upload Fix + CSV/Excel Support + ML Integration
   ============================================================================ */

// API Configuration
const API_BASE_URL = 'http://localhost:5000';
const API_ENDPOINTS = {
    uploadDataset: `${API_BASE_URL}/sl/upload-dataset`,
    trainModel: `${API_BASE_URL}/sl/train-model`,
    predict: `${API_BASE_URL}/sl/predict`
};

// Sri Lankan Cities
const SRI_LANKAN_CITIES = [
    'Colombo', 'Gampaha', 'Kalutara', 'Kandy', 'Matale', 'Nuwara Eliya',
    'Galle', 'Matara', 'Hambantota', 'Jaffna', 'Kilinochchi', 'Mannar',
    'Vavuniya', 'Mullaitivu', 'Batticaloa', 'Ampara', 'Trincomalee',
    'Kurunegala', 'Puttalam', 'Anuradhapura', 'Polonnaruwa', 'Badulla',
    'Monaragala', 'Ratnapura', 'Kegalle'
];

// Global State
let currentDataset = null;
let trainedModel = null;
let datasetStats = null;

// DOM Elements
const fileInput = document.getElementById('fileInput');
const selectFileBtn = document.getElementById('selectFileBtn');
const uploadZone = document.getElementById('uploadZone');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileMeta = document.getElementById('fileMeta');
const removeFileBtn = document.getElementById('removeFileBtn');
const previewCard = document.getElementById('previewCard');
const distributionCard = document.getElementById('distributionCard');
const trainModelBtn = document.getElementById('trainModelBtn');
const trainingProgress = document.getElementById('trainingProgress');
const resultsCard = document.getElementById('resultsCard');

/* ============================================================================
   FILE UPLOAD - EXCEL ONLY, MANUAL ANALYZE
   ============================================================================ */

let selectedFile = null;

// Initialize file upload handlers
function initFileUpload() {
    // Button click - triggers file input (opens ONCE)
    selectFileBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        fileInput.click();
    });

    // File input change - Store file, show info, DON'T auto-analyze
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            handleFileSelection(file);
        }
    });

    // Drag and drop handlers
    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('drag-over');
    });

    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('drag-over');
    });

    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('drag-over');

        const file = e.dataTransfer.files[0];
        if (file) {
            handleFileSelection(file);
        }
    });

    // Remove file button
    removeFileBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        resetFileUpload();
    });

    // Analyze file button - NEW: User must click this to analyze
    const analyzeBtn = document.getElementById('analyzeFileBtn');
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            if (selectedFile) {
                analyzeFile(selectedFile);
            } else {
                alert('Please select a file first.');
            }
        });
    }
}

/* ============================================================================
   FILE HANDLING - EXCEL ONLY
   ============================================================================ */

function handleFileSelection(file) {
    // Validate file type - EXCEL ONLY
    const validExtensions = ['.xlsx', '.xls'];
    const fileExtension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();

    if (!validExtensions.includes(fileExtension)) {
        alert('Invalid file format! Please upload Excel (.xlsx or .xls) files only.');
        fileInput.value = ''; // Reset
        return;
    }

    // Store file for later analysis
    selectedFile = file;

    // Display file info
    displayFileInfo(file);

    // Show analyze button
    const analyzeBtn = document.getElementById('analyzeFileBtn');
    if (analyzeBtn) {
        analyzeBtn.style.display = 'block';
    }
}

function displayFileInfo(file) {
    const sizeKB = (file.size / 1024).toFixed(2);
    const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
    const sizeText = file.size > 1024 * 1024 ? `${sizeMB} MB` : `${sizeKB} KB`;

    fileName.textContent = file.name;
    fileMeta.textContent = `${sizeText} • Excel File`;

    // Hide upload zone, show file info
    uploadZone.style.display = 'none';
    fileInfo.style.display = 'flex';
}

function resetFileUpload() {
    // Reset UI
    uploadZone.style.display = 'block';
    fileInfo.style.display = 'none';
    previewCard.style.display = 'none';
    distributionCard.style.display = 'none';
    resultsCard.style.display = 'none';
    trainModelBtn.disabled = true;

    // Hide analyze button
    const analyzeBtn = document.getElementById('analyzeFileBtn');
    if (analyzeBtn) {
        analyzeBtn.style.display = 'none';
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = '<i class="fas fa-chart-bar"></i> Analyze File';
    }

    // Reset state
    selectedFile = null;
    currentDataset = null;
    datasetStats = null;
    trainedModel = null;

    // Reset file input
    fileInput.value = '';
}

/* ============================================================================
   FILE ANALYSIS - EXCEL PROCESSING
   ============================================================================ */

async function analyzeFile(file) {
    console.log('Analyzing file:', file.name);

    // Show loading state
    const analyzeBtn = document.getElementById('analyzeFileBtn');
    if (analyzeBtn) {
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
    }

    try {
        // Process Excel file
        await processExcelFile(file);
    } catch (error) {
        console.error('Analysis error:', error);
        alert(`Failed to analyze file: ${error.message}`);

        // Reset button
        if (analyzeBtn) {
            analyzeBtn.disabled = false;
            analyzeBtn.innerHTML = '<i class="fas fa-chart-bar"></i> Analyze File';
        }
    }
}

/* ============================================================================
   EXCEL PROCESSING - UPLOAD TO BACKEND
   ============================================================================ */

function processExcelFile(file) {
    return new Promise((resolve, reject) => {
        console.log('Processing Excel file:', file.name);

        // Upload directly to backend for processing
        uploadToBackend(file)
            .then(() => {
                console.log('Excel file processed successfully');
                resolve();
            })
            .catch((error) => {
                console.error('Excel processing failed:', error);
                reject(error);
            });
    });
}

/* ============================================================================
   BACKEND UPLOAD & DATASET ANALYSIS
   ============================================================================ */

async function uploadToBackend(file) {
    try {
        console.log('Uploading to backend:', file.name);

        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(API_ENDPOINTS.uploadDataset, {
            method: 'POST',
            body: formData
        });

        console.log('Response status:', response.status);

        if (!response.ok) {
            const errorText = await response.text();
            console.error('Upload failed:', errorText);
            throw new Error(`Upload failed: ${response.statusText}`);
        }

        const result = await response.json();
        console.log('Upload result:', result);

        if (result.status === 'success') {
            datasetStats = result;
            displayDatasetPreview(result.preview);
            displayClassDistribution(result.distribution);
            trainModelBtn.disabled = false;

            // Hide analyze button after successful analysis
            const analyzeBtn = document.getElementById('analyzeFileBtn');
            if (analyzeBtn) {
                analyzeBtn.style.display = 'none';
            }

            console.log('Dataset loaded successfully:', result.total_rows, 'rows');
        } else {
            throw new Error(result.message || 'Upload failed');
        }
    } catch (error) {
        console.error('Upload error:', error);
        alert(`Failed to analyze dataset: ${error.message}\n\nPlease check:\n1. Backend server is running\n2. File is a valid Excel file\n3. File has required columns`);

        // Reset analyze button
        const analyzeBtn = document.getElementById('analyzeFileBtn');
        if (analyzeBtn) {
            analyzeBtn.disabled = false;
            analyzeBtn.innerHTML = '<i class="fas fa-chart-bar"></i> Analyze File';
        }

        throw error;
    }
}

/* ============================================================================
   DATASET PREVIEW DISPLAY
   ============================================================================ */

function displayDatasetPreview(preview) {
    if (!preview || preview.length === 0) return;

    // Show preview card
    previewCard.style.display = 'block';

    // Update row count
    document.getElementById('rowCount').textContent = `${datasetStats.total_rows} rows`;

    // Get headers
    const headers = Object.keys(preview[0]);

    // Build table header
    const thead = document.getElementById('previewTableHead');
    thead.innerHTML = '<tr>' + headers.map(h => `<th>${h}</th>`).join('') + '</tr>';

    // Build table body (first 10 rows)
    const tbody = document.getElementById('previewTableBody');
    tbody.innerHTML = preview.map(row => {
        return '<tr>' + headers.map(h => {
            let value = row[h];
            // Highlight Sri Lankan cities
            if (SRI_LANKAN_CITIES.includes(value)) {
                value = `<span style="color: var(--sl-orange); font-weight: 600;">${value}</span>`;
            }
            return `<td>${value}</td>`;
        }).join('') + '</tr>';
    }).join('');
}

/* ============================================================================
   CLASS DISTRIBUTION DISPLAY
   ============================================================================ */

function displayClassDistribution(distribution) {
    if (!distribution) return;

    // Show distribution card
    distributionCard.style.display = 'block';

    // Display stats
    const statsContainer = document.getElementById('distributionStats');
    const total = datasetStats.total_rows;

    statsContainer.innerHTML = `
        <div class="stat-box">
            <div class="stat-label">Safe (Class 0)</div>
            <div class="stat-value">${distribution['0'] || 0}</div>
            <div class="stat-percentage">${((distribution['0'] / total) * 100).toFixed(1)}%</div>
        </div>
        <div class="stat-box">
            <div class="stat-label">Suspicious (Class 1)</div>
            <div class="stat-value">${distribution['1'] || 0}</div>
            <div class="stat-percentage">${((distribution['1'] / total) * 100).toFixed(1)}%</div>
        </div>
    `;

    // Create pie chart
    createDistributionChart(distribution);
}

function createDistributionChart(distribution) {
    const ctx = document.getElementById('distributionChart');

    // Destroy existing chart if any
    if (window.distributionChartInstance) {
        window.distributionChartInstance.destroy();
    }

    window.distributionChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Safe (0)', 'Suspicious (1)'],
            datasets: [{
                data: [distribution['0'] || 0, distribution['1'] || 0],
                backgroundColor: [
                    'rgba(16, 185, 129, 0.8)',
                    'rgba(239, 68, 68, 0.8)'
                ],
                borderColor: [
                    'rgba(16, 185, 129, 1)',
                    'rgba(239, 68, 68, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#94a3b8',
                        font: {
                            size: 14
                        }
                    }
                }
            }
        }
    });
}

/* ============================================================================
   ML MODEL TRAINING
   ============================================================================ */

trainModelBtn.addEventListener('click', async () => {
    const modelType = document.getElementById('modelType').value;
    const testSize = parseInt(document.getElementById('testSize').value) / 100;

    // Show training progress
    trainingProgress.style.display = 'block';
    trainModelBtn.disabled = true;

    try {
        const response = await fetch(API_ENDPOINTS.trainModel, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model_type: modelType,
                test_size: testSize
            })
        });

        if (!response.ok) {
            throw new Error(`Training failed: ${response.statusText}`);
        }

        const result = await response.json();

        if (result.status === 'success') {
            trainedModel = result;
            displayModelResults(result);
            buildPredictionForm();
        } else {
            throw new Error(result.message || 'Training failed');
        }
    } catch (error) {
        console.error('Training error:', error);
        alert(`Failed to train model: ${error.message}`);
    } finally {
        trainingProgress.style.display = 'none';
        trainModelBtn.disabled = false;
    }
});

/* ============================================================================
   INITIALIZATION
   ============================================================================ */

/* ============================================================================
   MODEL RESULTS DISPLAY
   ============================================================================ */

function displayModelResults(result) {
    // Show results card
    resultsCard.style.display = 'block';

    // Display metrics
    const metricsGrid = document.getElementById('metricsGrid');
    metricsGrid.innerHTML = `
        <div class="metric-card">
            <div class="metric-label">Accuracy</div>
            <div class="metric-value">${(result.metrics.accuracy * 100).toFixed(2)}%</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Precision</div>
            <div class="metric-value">${(result.metrics.precision * 100).toFixed(2)}%</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Recall</div>
            <div class="metric-value">${(result.metrics.recall * 100).toFixed(2)}%</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">F1 Score</div>
            <div class="metric-value">${(result.metrics.f1_score * 100).toFixed(2)}%</div>
        </div>
    `;

    // Display confusion matrix
    const confusionMatrix = document.getElementById('confusionMatrix');
    const cm = result.confusion_matrix;
    confusionMatrix.innerHTML = `
        <h3>Confusion Matrix</h3>
        <div class="matrix-grid">
            <div class="matrix-cell">
                <div class="matrix-cell-label">True Negative</div>
                <div class="matrix-cell-value">${cm[0][0]}</div>
            </div>
            <div class="matrix-cell">
                <div class="matrix-cell-label">False Positive</div>
                <div class="matrix-cell-value">${cm[0][1]}</div>
            </div>
            <div class="matrix-cell">
                <div class="matrix-cell-label">False Negative</div>
                <div class="matrix-cell-value">${cm[1][0]}</div>
            </div>
            <div class="matrix-cell">
                <div class="matrix-cell-label">True Positive</div>
                <div class="matrix-cell-value">${cm[1][1]}</div>
            </div>
        </div>
    `;
}

/* ============================================================================
   PREDICTION FORM BUILDER
   ============================================================================ */

function buildPredictionForm() {
    const form = document.getElementById('predictionForm');

    // Get feature names from trained model
    const features = trainedModel.features || [];

    if (features.length === 0) {
        form.innerHTML = '<p style="color: var(--text-secondary);">No features available for prediction.</p>';
        return;
    }

    // Build form fields
    let formHTML = '';

    features.forEach(feature => {
        if (feature === 'current_city' || feature === 'previous_city') {
            // Dropdown for cities
            formHTML += `
                <div class="form-group">
                    <label for="pred_${feature}">${formatLabel(feature)}</label>
                    <select id="pred_${feature}" name="${feature}" class="form-control" required>
                        <option value="">Select City</option>
                        ${SRI_LANKAN_CITIES.map(city => `<option value="${city}">${city}</option>`).join('')}
                    </select>
                </div>
            `;
        } else if (feature.includes('flag') || feature.includes('roaming')) {
            // Checkbox for boolean fields
            formHTML += `
                <div class="form-group">
                    <label>
                        <input type="checkbox" id="pred_${feature}" name="${feature}" value="1">
                        ${formatLabel(feature)}
                    </label>
                </div>
            `;
        } else {
            // Number input for numeric fields
            formHTML += `
                <div class="form-group">
                    <label for="pred_${feature}">${formatLabel(feature)}</label>
                    <input type="number" id="pred_${feature}" name="${feature}" class="form-control" step="0.01" required>
                </div>
            `;
        }
    });

    formHTML += `
        <button type="submit" class="btn btn-primary btn-block">
            <i class="fas fa-bolt"></i> Predict
        </button>
        <div id="predictionResult" style="display: none; margin-top: 1rem;"></div>
    `;

    form.innerHTML = formHTML;

    // Add submit handler
    form.addEventListener('submit', handlePrediction);
}

function formatLabel(fieldName) {
    return fieldName
        .replace(/_/g, ' ')
        .replace(/\b\w/g, l => l.toUpperCase());
}

/* ============================================================================
   LIVE PREDICTION
   ============================================================================ */

async function handlePrediction(e) {
    e.preventDefault();

    const formData = new FormData(e.target);
    const data = {};

    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }

    try {
        const response = await fetch(API_ENDPOINTS.predict, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`Prediction failed: ${response.statusText}`);
        }

        const result = await response.json();
        displayPredictionResult(result);
    } catch (error) {
        console.error('Prediction error:', error);
        alert(`Failed to make prediction: ${error.message}`);
    }
}

function displayPredictionResult(result) {
    const resultDiv = document.getElementById('predictionResult');

    const isSuspicious = result.prediction === 1;
    const confidence = (result.confidence * 100).toFixed(2);

    resultDiv.innerHTML = `
        <div style="padding: 1rem; border-radius: 0.5rem; background: ${isSuspicious ? 'rgba(239, 68, 68, 0.1)' : 'rgba(16, 185, 129, 0.1)'}; border: 2px solid ${isSuspicious ? 'var(--accent-red)' : 'var(--accent-green)'};">
            <h3 style="margin-bottom: 0.5rem; color: ${isSuspicious ? 'var(--accent-red)' : 'var(--accent-green)'};">
                ${isSuspicious ? '🚨 SUSPICIOUS' : '✅ SAFE'}
            </h3>
            <p style="color: var(--text-secondary);">Confidence: ${confidence}%</p>
        </div>
    `;

    resultDiv.style.display = 'block';
}

/* ============================================================================
   INITIALIZATION
   ============================================================================ */

document.addEventListener('DOMContentLoaded', () => {
    initFileUpload();
    console.log('🇱🇰 Sri Lankan ML Dashboard initialized');
});

    // Reset file input
    fileInput.value = '';
}

/* ============================================================================
   END OF FILE
   ============================================================================ */
