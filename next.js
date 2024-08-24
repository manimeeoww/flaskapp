import React from 'react';

const HomePage = () => {
  return (
    <div>
      <h1>Welcome to Petal Pedia</h1>
      <p>Upload a flower image to see its details.</p>
      <form id="upload-form" enctype="multipart/form-data">
        <input type="file" id="file-input" name="file" accept="image/*" />
        <button type="button" onClick={() => getPrediction()}>Upload and Predict</button>
      </form>
      <div id="prediction-result"></div>
      <div id="flower-info"></div>
    </div>
  );
};

export default HomePage;
