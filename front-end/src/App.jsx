import React, { useState } from 'react';

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);

    // Send the file to Flask backend
    const response = await fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();
    setResult(data); // Save the returned data to state
  };

  return (
    <div>
      <h1>PCAP File Analyzer</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload and Analyze</button>

      {result && (
        <div>
          <h2>Analysis Result</h2>
          {result.Feature.map((feature, index) => (
            <p key={index}>{feature}: {result.Value[index]}</p>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
