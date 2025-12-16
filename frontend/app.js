// -----------------------------------------------------------------------------
// !! IMPORTANT !!
// GANTI URL DI BAWAH INI DENGAN URL BACKEND RAILWAY ANDA
// Contoh: const API_URL = 'https://backend-anda-di-railway.up.railway.app';
// -----------------------------------------------------------------------------
const API_URL = 'https://deteksi-kerusakan-backend.up.railway.app';
// -----------------------------------------------------------------------------

console.log('API URL:', API_URL);

// DOM Elements
const uploadSection = document.getElementById('uploadSection');
const fileInput = document.getElementById('fileInput');
const previewImage = document.getElementById('previewImage');
const canvas = document.getElementById('canvas');
const resultContainer = document.getElementById('resultContainer');
const detectionsList = document.getElementById('detectionsList');
const loadingSpinner = document.getElementById('loadingSpinner');

// File upload handlers
uploadSection.addEventListener('click', () => fileInput.click());

uploadSection.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadSection.classList.add('drag-active');
});

uploadSection.addEventListener('dragleave', () => {
    uploadSection.classList.remove('drag-active');
});

uploadSection.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadSection.classList.remove('drag-active');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

async function handleFile(file) {
    // Validate file
    if (!file.type.startsWith('image/')) {
        alert('Please select an image file');
        return;
    }

    if (file.size > 10 * 1024 * 1024) {
        alert('File size must be less than 10MB');
        return;
    }

    // Show loading
    loadingSpinner.style.display = 'flex';
    resultContainer.style.display = 'none';
    detectionsList.innerHTML = '';

    try {
        // Read and display image
        const reader = new FileReader();
        reader.onload = async (e) => {
            previewImage.src = e.target.result;
            previewImage.onload = async () => {
                // Send to backend
                const formData = new FormData();
                formData.append('file', file);

                console.log('Sending request to:', `${API_URL}/detect`);
                
                const response = await fetch(`${API_URL}/detect`, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'Accept': 'application/json'
                    }
                });

                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({}));
                    throw new Error(errorData.detail || `Server error: ${response.status}`);
                }

                const data = await response.json();
                console.log('Response:', data);
                
                // Display results
                displayResults(data);
                loadingSpinner.style.display = 'none';
                resultContainer.style.display = 'block';
            };
        };
        reader.readAsDataURL(file);
    } catch (error) {
        console.error('Error:', error);
        alert(`Error: ${error.message}`);
        loadingSpinner.style.display = 'none';
    }
}

function displayResults(data) {
    // Clear previous detections
    detectionsList.innerHTML = '';
    
    if (!data.detections || data.detections.length === 0) {
        detectionsList.innerHTML = '<div style="padding: 20px; text-align: center; color: #888;">No defects detected ✓</div>';
        drawOnCanvas([]);
        return;
    }

    // Display detections
    data.detections.forEach((detection, index) => {
        const item = document.createElement('div');
        item.className = `detection-item severity-${detection.severity.toLowerCase()}`;
        item.innerHTML = `
            <div class="detection-header">
                <span class="detection-class">${detection.class_name}</span>
                <span class="severity-badge">${detection.severity}</span>
            </div>
            <div class="detection-details">
                <p>Confidence: <strong>${(detection.confidence * 100).toFixed(1)}%</strong></p>
                <p>Position: x=${Math.round(detection.x)}, y=${Math.round(detection.y)}</p>
                <p>Size: ${Math.round(detection.width)}×${Math.round(detection.height)}px</p>
            </div>
        `;
        detectionsList.appendChild(item);
    });

    // Draw on canvas
    drawOnCanvas(data.detections);
}

function drawOnCanvas(detections) {
    const ctx = canvas.getContext('2d');
    const img = new Image();
    img.src = previewImage.src;
    
    img.onload = () => {
        // Set canvas size
        canvas.width = img.width;
        canvas.height = img.height;

        // Draw image
        ctx.drawImage(img, 0, 0);

        // Draw detections
        detections.forEach(detection => {
            const severityColors = {
                'HIGH': '#FF6B6B',
                'MEDIUM': '#FFA500',
                'LOW': '#4ECDC4'
            };

            const color = severityColors[detection.severity] || '#FFFFFF';

            // Draw bounding box
            ctx.strokeStyle = color;
            ctx.lineWidth = 3;
            ctx.strokeRect(
                detection.x,
                detection.y,
                detection.width,
                detection.height
            );

            // Draw label background
            const label = `${detection.class_name} (${(detection.confidence * 100).toFixed(0)}%)`;
            const fontSize = 14;
            ctx.font = `bold ${fontSize}px Arial`;
            const textMetrics = ctx.measureText(label);
            const textWidth = textMetrics.width + 8;
            const textHeight = fontSize + 6;

            ctx.fillStyle = color;
            ctx.fillRect(
                detection.x,
                detection.y - textHeight - 4,
                textWidth,
                textHeight
            );

            // Draw label text
            ctx.fillStyle = '#FFFFFF';
            ctx.textBaseline = 'top';
            ctx.fillText(label, detection.x + 4, detection.y - textHeight);
        });
    };
}
