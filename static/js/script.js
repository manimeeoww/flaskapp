// script.js

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
        const response = await fetch('https://petalpedia-ai-manimeeowws-projects.vercel.app/', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const result = await response.json();

            if (result.prediction) {
                predictionResult.innerText = 'Prediction: ' + result.prediction;
                flowerInfoDiv.innerHTML = `
                    <img src="${result.image}" alt="${result.prediction}">
                    <h2>${result.prediction}</h2>
                    <p><strong>Scientific Name:</strong> ${result.scientific_name || 'N/A'}</p>
                    <p><strong>Origin:</strong> ${result.origin || 'N/A'}</p>
                    <p><strong>Family:</strong> ${result.family || 'N/A'}</p>
                    <p><strong>Symbolism:</strong> ${result.symbolism || 'N/A'}</p>
                    <p>${result.link ? `<a href="${result.link}" target="_blank">Learn More</a>` : ''}</p>
                `;
            } else {
                predictionResult.innerText = 'Prediction data not found.';
            }
        } else {
            const error = await response.json();
            predictionResult.innerText = 'Error: ' + (error.error || 'Unknown error occurred.');
        }
    } catch (error) {
        predictionResult.innerText = 'Error: Unable to reach the server. Please try again later.';
        console.error('Fetch error:', error); // Log error details to the console
    }
}

