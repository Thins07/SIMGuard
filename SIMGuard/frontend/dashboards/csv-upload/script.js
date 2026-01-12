// Global variables
let uploadedFile = null;
let analysisResults = null;
let detectionChart = null;

// Backend API configuration
const API_BASE_URL = 'http://localhost:5000';
const API_ENDPOINTS = {
    upload: `${API_BASE_URL}/upload`,
    analyze: `${API_BASE_URL}/analyze`,
    results: `${API_BASE_URL}/results`,
    report: `${API_BASE_URL}/report`,
    status: `${API_BASE_URL}/status`,
    clear: `${API_BASE_URL}/clear`
};

// DOM Elements
const fileInput = document.getElementById('fileInput');
const uploadBox = document.getElementById('uploadBox');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const fileType = document.getElementById('fileType');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    initializeNavigation();
});

// Initialize event listeners
function initializeEventListeners() {
    // File upload events
    fileInput.addEventListener('change', handleFileSelect);
    uploadBox.addEventListener('click', () => fileInput.click());
    uploadBox.addEventListener('dragover', handleDragOver);
    uploadBox.addEventListener('dragleave', handleDragLeave);
    uploadBox.addEventListener('drop', handleFileDrop);
    
    // Navigation events
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', handleNavigation);
    });
    
    // Mobile menu toggle
    const hamburger = document.querySelector('.hamburger');
    if (hamburger) {
        hamburger.addEventListener('click', toggleMobileMenu);
    }
}

// Navigation functionality
function initializeNavigation() {
    // Smooth scrolling for navigation links
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
    
    // Update active navigation on scroll
    window.addEventListener('scroll', updateActiveNavigation);
}

function handleNavigation(e) {
    e.preventDefault();
    const targetId = e.target.getAttribute('href');
    const targetSection = document.querySelector(targetId);
    
    if (targetSection) {
        targetSection.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
    
    // Update active state
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    e.target.classList.add('active');
}

function updateActiveNavigation() {
    const sections = document.querySelectorAll('.section');
    const navLinks = document.querySelectorAll('.nav-link');
    
    let currentSection = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop - 100;
        const sectionHeight = section.offsetHeight;
        if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
            currentSection = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${currentSection}`) {
            link.classList.add('active');
        }
    });
}

function toggleMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    navMenu.classList.toggle('active');
}

function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// File upload functionality
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        processFile(file);
    }
}

function handleDragOver(e) {
    e.preventDefault();
    uploadBox.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadBox.classList.remove('dragover');
}

function handleFileDrop(e) {
    e.preventDefault();
    uploadBox.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        const file = files[0];
        if (isValidFileType(file)) {
            processFile(file);
        } else {
            showError('Please upload a CSV or JSON file.');
        }
    }
}

function isValidFileType(file) {
    const validTypes = ['text/csv', 'application/json', '.csv', '.json'];
    return validTypes.some(type => 
        file.type === type || file.name.toLowerCase().endsWith(type)
    );
}

function processFile(file) {
    uploadedFile = file;
    
    // Display file information
    fileName.textContent = file.name;
    fileSize.textContent = `Size: ${formatFileSize(file.size)}`;
    fileType.textContent = `Type: ${file.type || 'Unknown'}`;
    
    // Show file info section
    fileInfo.style.display = 'block';
    uploadBox.style.display = 'none';
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// File analysis functionality
async function analyzeFile() {
    if (!uploadedFile) {
        showError('No file uploaded.');
        return;
    }

    // Show loading state
    const analyzeBtn = document.querySelector('.analyze-btn');
    const originalText = analyzeBtn.innerHTML;
    analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Uploading...';
    analyzeBtn.disabled = true;

    try {
        // Step 1: Upload file to backend
        const formData = new FormData();
        formData.append('file', uploadedFile);

        const uploadResponse = await fetch(API_ENDPOINTS.upload, {
            method: 'POST',
            body: formData
        });

        if (!uploadResponse.ok) {
            const errorData = await uploadResponse.json();
            throw new Error(errorData.message || 'Upload failed');
        }

        const uploadResult = await uploadResponse.json();
        console.log('Upload successful:', uploadResult);

        // Step 2: Trigger analysis
        analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';

        const analyzeResponse = await fetch(API_ENDPOINTS.analyze, {
            method: 'POST'
        });

        if (!analyzeResponse.ok) {
            const errorData = await analyzeResponse.json();
            throw new Error(errorData.message || 'Analysis failed');
        }

        const analyzeResult = await analyzeResponse.json();
        console.log('Analysis successful:', analyzeResult);

        // Step 3: Get detailed results
        analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading Results...';

        const resultsResponse = await fetch(API_ENDPOINTS.results);

        if (!resultsResponse.ok) {
            const errorData = await resultsResponse.json();
            throw new Error(errorData.message || 'Failed to get results');
        }

        analysisResults = await resultsResponse.json();
        console.log('Results retrieved:', analysisResults);

        // Display results
        displayResults(analysisResults);

        // Reset button
        analyzeBtn.innerHTML = originalText;
        analyzeBtn.disabled = false;

        // Show results section
        document.getElementById('results').style.display = 'block';
        document.getElementById('report').style.display = 'block';

        // Scroll to results
        scrollToSection('results');

        showSuccess('Analysis completed successfully!');

    } catch (error) {
        console.error('Analysis error:', error);
        showError(`Analysis failed: ${error.message}`);

        // Reset button
        analyzeBtn.innerHTML = originalText;
        analyzeBtn.disabled = false;
    }
}

function generateMockResults() {
    const totalRecords = Math.floor(Math.random() * 1000) + 500;
    const suspiciousCount = Math.floor(Math.random() * 50) + 5;
    const cleanCount = totalRecords - suspiciousCount;
    
    const suspiciousRecords = [];
    const flagReasons = [
        'Unusual location change',
        'Multiple SIM activations',
        'Suspicious IP address',
        'Device fingerprint mismatch',
        'Rapid account access',
        'Anomalous behavior pattern',
        'Geolocation inconsistency',
        'Time-based anomaly'
    ];
    
    const riskLevels = ['High', 'Medium', 'Low'];
    
    for (let i = 0; i < suspiciousCount; i++) {
        const timestamp = new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000);
        suspiciousRecords.push({
            timestamp: timestamp.toISOString().slice(0, 19).replace('T', ' '),
            userId: `USR${String(Math.floor(Math.random() * 10000)).padStart(4, '0')}`,
            simId: `SIM${String(Math.floor(Math.random() * 100000)).padStart(5, '0')}`,
            ipAddress: generateRandomIP(),
            deviceId: `DEV${String(Math.floor(Math.random() * 100000)).padStart(5, '0')}`,
            flagReason: flagReasons[Math.floor(Math.random() * flagReasons.length)],
            riskLevel: riskLevels[Math.floor(Math.random() * riskLevels.length)]
        });
    }
    
    return {
        totalRecords,
        suspiciousCount,
        cleanCount,
        suspiciousRecords: suspiciousRecords.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
    };
}

function generateRandomIP() {
    return `${Math.floor(Math.random() * 256)}.${Math.floor(Math.random() * 256)}.${Math.floor(Math.random() * 256)}.${Math.floor(Math.random() * 256)}`;
}

function displayResults(results) {
    // Update statistics from backend response
    document.getElementById('recordsProcessed').textContent = results.summary.total_records.toLocaleString();
    document.getElementById('suspiciousActivities').textContent = results.summary.suspicious_count.toLocaleString();
    document.getElementById('cleanRecords').textContent = results.summary.clean_count.toLocaleString();

    // Create chart
    createDetectionChart(results);

    // Populate table
    populateSuspiciousTable(results.suspicious_activities);
}

function createDetectionChart(results) {
    const ctx = document.getElementById('detectionChart').getContext('2d');

    // Destroy existing chart if it exists
    if (detectionChart) {
        detectionChart.destroy();
    }

    detectionChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Clean Records', 'Suspicious Activities'],
            datasets: [{
                data: [results.summary.clean_count, results.summary.suspicious_count],
                backgroundColor: ['#10b981', '#ef4444'],
                borderColor: ['#059669', '#dc2626'],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#cbd5e1',
                        padding: 20,
                        font: {
                            family: 'Inter',
                            size: 12
                        }
                    }
                }
            }
        }
    });
}

function populateSuspiciousTable(records) {
    const tableBody = document.getElementById('suspiciousTableBody');
    tableBody.innerHTML = '';

    records.forEach(record => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${record.timestamp}</td>
            <td>${record.user_id}</td>
            <td>${record.sim_id}</td>
            <td>${record.ip}</td>
            <td>${record.device_id}</td>
            <td>${record.flag_reason}</td>
            <td><span class="risk-${record.risk_level.toLowerCase()}">${record.risk_level}</span></td>
        `;
        tableBody.appendChild(row);
    });
}

// Report generation
async function downloadReport() {
    if (!analysisResults) {
        showError('No analysis results available.');
        return;
    }

    try {
        // Show loading state
        const downloadBtn = document.querySelector('.download-btn');
        const originalText = downloadBtn.innerHTML;
        downloadBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating Report...';
        downloadBtn.disabled = true;

        // Request report from backend
        const response = await fetch(API_ENDPOINTS.report);

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Report generation failed');
        }

        // Get the PDF blob
        const blob = await response.blob();

        // Create download link
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `SIMGuard_Investigation_Report_${new Date().toISOString().slice(0, 10)}.pdf`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);

        // Reset button
        downloadBtn.innerHTML = originalText;
        downloadBtn.disabled = false;

        showSuccess('Investigation report downloaded successfully!');

    } catch (error) {
        console.error('Report download error:', error);
        showError(`Report download failed: ${error.message}`);

        // Reset button
        const downloadBtn = document.querySelector('.download-btn');
        downloadBtn.innerHTML = '<i class="fas fa-download"></i> Download Investigation Report';
        downloadBtn.disabled = false;
    }
}

function generateReportContent(results) {
    const timestamp = new Date().toISOString();
    
    let content = `
SIMGuard Investigation Report
Generated: ${timestamp}
File Analyzed: ${uploadedFile.name}

EXECUTIVE SUMMARY
================
Total Records Processed: ${results.totalRecords}
Suspicious Activities Detected: ${results.suspiciousCount}
Clean Records: ${results.cleanCount}
Risk Assessment: ${results.suspiciousCount > 20 ? 'HIGH' : results.suspiciousCount > 10 ? 'MEDIUM' : 'LOW'}

DETAILED FINDINGS
================
`;

    results.suspiciousRecords.forEach((record, index) => {
        content += `
${index + 1}. Suspicious Activity
   Timestamp: ${record.timestamp}
   User ID: ${record.userId}
   SIM ID: ${record.simId}
   IP Address: ${record.ipAddress}
   Device ID: ${record.deviceId}
   Flag Reason: ${record.flagReason}
   Risk Level: ${record.riskLevel}
`;
    });

    content += `

RECOMMENDATIONS
==============
1. Investigate high-risk activities immediately
2. Implement additional authentication for flagged users
3. Monitor suspicious IP addresses
4. Review SIM activation procedures
5. Consider implementing real-time monitoring

TECHNICAL METADATA
==================
Analysis Engine: SIMGuard AI v1.0
Detection Algorithm: Behavioral Analytics + Machine Learning
Confidence Level: 95%
Processing Time: ${(2 + Math.random() * 2).toFixed(2)} seconds

This report is generated for digital forensics and security investigation purposes.
`;

    return content;
}

// Utility functions
function showError(message) {
    // Simple error display - could be enhanced with a proper notification system
    alert('Error: ' + message);
}

function showSuccess(message) {
    // Simple success display - could be enhanced with a proper notification system
    alert('Success: ' + message);
}
