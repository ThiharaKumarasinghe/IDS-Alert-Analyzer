import React, { useState } from "react"; 

const XAI = () => {
  const [isTraining, setIsTraining] = useState(false);
  const [statusMessage, setStatusMessage] = useState("");
  const [cluster6Result, setCluster6Result] = useState(null); // To store the result for Cluster 6

  // Function to start the training
  const startTraining = async () => {
    setStatusMessage('Model is training...');
    setIsTraining(true);
  
    try {
      const response = await fetch('http://localhost:5000/api/train-xai-model', { method: 'GET' });
      if (!response.ok) {
        throw new Error('Error starting model training');
      }
  
      const intervalId = setInterval(async () => {
        const statusResponse = await fetch('http://localhost:5000/api/training-status', { method: 'GET' });
        const status = await statusResponse.json();
  
        if (!status.is_training) {
          setStatusMessage('Training complete!');
          setIsTraining(false);
          clearInterval(intervalId);
        }
      }, 2000);
    } catch (error) {
      console.error('Error during training:', error);
      setStatusMessage('An error occurred during training.');
      setIsTraining(false);
    }
  };

  // Function to fetch aggregate explanations for a cluster
  const getClusterExplanations = async (clusterName) => {
    setStatusMessage(`Fetching explanations for Cluster ${clusterName}...`);
    try {
      const response = await fetch(`http://localhost:5000/api/cluster/${clusterName}/xai`, { method: 'GET' });
      if (!response.ok) {
        throw new Error('Error fetching explanations');
      }

      const data = await response.json();
      setCluster6Result(data.result); // Store the result in state
      setStatusMessage('Explanations fetched successfully');
      console.log(cluster6Result)
    } catch (error) {
      console.error('Error fetching explanations:', error);
      setStatusMessage('An error occurred while fetching explanations.');
    }
  };

  return (
    <div>
      {/* Button to start training */}
      <button
        onClick={startTraining}
        disabled={isTraining}
        className="bg-black text-white p-4 rounded-2xl"
      >
        {isTraining ? "Training in Progress..." : "Start Training"}
      </button>

      {/* Button to fetch explanations for Cluster 6 */}
      <button
        onClick={() => getClusterExplanations(6)} // Pass clusterName as a parameter
        className="bg-blue-500 text-white p-4 rounded-2xl ml-4"
      >
        Fetch Explanations for Cluster 6
      </button>

      {/* Status message */}
      <p>{statusMessage}</p>

      {/* Display the result for Cluster 6 */}
      {cluster6Result && (
        <div>
          <h2>Cluster 6 Explanations:</h2>
          <pre>{JSON.stringify(cluster6Result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default XAI;
