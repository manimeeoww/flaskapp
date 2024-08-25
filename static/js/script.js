async function getPrediction() {
    const fileInput = document.getElementById('file-input');
    const predictionResult = document.getElementById('prediction-result');
    const flowerInfoDiv = document.getElementById('flower-info');
    const formData = new FormData();

    // Clear previous results
    predictionResult.innerText = '';
    flowerInfoDiv.innerHTML = '';

    // Check if a file is selected
    if (fileInput.files.length === 0) {
        predictionResult.innerText = 'Please select a file to upload.';
        return;
    }

    formData.append('file', fileInput.files[0]);

    // Set loading state
    predictionResult.innerText = 'Processing... Please wait.';

    try {
        const response = await fetch('http://localhost:5000/predict', {  // Ensure this URL matches your Flask app's URL
            method: 'POST',
            body: formData,
            headers: {
                'Accept': 'application/json'  // Set to expect JSON response
            }
        });

        if (response.ok) {
            const result = await response.json();
            predictionResult.innerText = 'Prediction: ' + result.prediction;
            flowerInfoDiv.innerHTML = `
                <img src="${result.image}" alt="${result.prediction}" width="200" height="200">
                <h2>${result.prediction}</h2>
                <p><strong>Scientific Name:</strong> ${result.scientific_name || 'N/A'}</p>
                <p><strong>Origin:</strong> ${result.origin || 'N/A'}</p>
                <p><strong>Family:</strong> ${result.family || 'N/A'}</p>
                <p><strong>Symbolism:</strong> ${result.symbolism || 'N/A'}</p>
                ${result.link ? `<p><a href="${result.link}" target="_blank">Learn More</a></p>` : ''}
            `;
        } else {
            const error = await response.json();
            predictionResult.innerText = 'Error: ' + (error.error || 'Unknown error occurred.');
        }
    } catch (error) {
        predictionResult.innerText = 'Fetch error: ' + error.message;
        console.error('Fetch error:', error);
    }
}


