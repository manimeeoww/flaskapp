import React, { useState } from 'react';

const HomePage = () => {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const getPrediction = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/predict', {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        const data = await response.json();
        setResult(data);
        setError(null);
      } else {
        const errorData = await response.json();
        setError(errorData.error || 'Error occurred');
      }
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div>
      <h1>Flower Classification</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={getPrediction}>Upload and Predict</button>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {result && (
        <div>
          <h2>Prediction: {result.prediction}</h2>
          <img src={result.image} alt={result.prediction} style={{ maxWidth: '300px', height: 'auto' }} />
          <p><strong>Scientific Name:</strong> {result.scientific_name}</p>
          <p><strong>Origin:</strong> {result.origin}</p>
          <p><strong>Family:</strong> {result.family}</p>
          <p><strong>Symbolism:</strong> {result.symbolism}</p>
          <p><a href={result.link} target="_blank">Learn More</a></p>
        </div>
      )}
    </div>
  );
};

export default HomePage;

