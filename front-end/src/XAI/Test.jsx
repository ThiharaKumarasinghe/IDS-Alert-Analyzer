import React, { useState } from "react";

const XAI = () => {
  const [isTraining, setIsTraining] = useState(false);
  const [statusMessage, setStatusMessage] = useState("");
  const [clusterResult, setClusterResult] = useState(null);
  const [explanation, setExplanation] = useState(null);

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



  // Function to fetch the result for a cluster
  const getClusterExplanations = async (clusterName) => {
    setStatusMessage(`Fetching explanations for Cluster ${clusterName}...`);
    try {
      const response = await fetch(
        `http://localhost:5000/api/cluster/${clusterName}/xai`,
        { method: "GET" }
      );
      if (!response.ok) {
        throw new Error("Error fetching explanations");
      }

      const data = await response.json();
      setClusterResult(data.result); // Store the result in state
      setStatusMessage("Explanations fetched successfully");
    } catch (error) {
      console.error("Error fetching explanations:", error);
      setStatusMessage("Error occurred while fetching explanations.");
    }
  };

  // Function to explain the cluster result
const explainCluster = async (clusterResult) => {
  console.log(clusterResult)
  setStatusMessage("Fetching explanation...");

  try {
    const response = await fetch("http://localhost:5000/api/explain-cluster", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ cluster_result: clusterResult }),
    });

    if (!response.ok) {
      throw new Error("Error fetching explanation");
    }

    const data = await response.json();
    setExplanation(data.explanation); // Store the explanation in state
    setStatusMessage("Explanation fetched successfully");
  } catch (error) {
    console.error("Error fetching explanation:", error);
    setStatusMessage("Error occurred while fetching explanation.");
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

      {/* Button to fetch explanations for a specific cluster */}
      <button
        onClick={() => getClusterExplanations(1)} // Fetch explanations for Cluster 6
        className="bg-blue-500 text-white p-4 rounded-2xl ml-4"
      >
        Fetch Explanations for Cluster 6
      </button>

      {/* Status message */}
      <p>{statusMessage}</p>

      {/* Display cluster results */}
      {clusterResult && (
        <div>
          <h2>Cluster 6 Results:</h2>
          <pre>{JSON.stringify(clusterResult, null, 2)}</pre>

          {/* Button to get explanation for the result */}
          <button
            onClick={() =>
              explainCluster(clusterResult)
               // Directly pass clusterResult
            }
            className="bg-green-500 text-white p-4 rounded-2xl mt-4"
          >
            Explain This Result
          </button>
        </div>
      )}

      {/* Display explanation */}
      {explanation && (
        <div>
          <h2>Explanation for Cluster 6:</h2>
          <pre>{explanation}</pre>
        </div>
      )}
    </div>
  );
};

export default XAI;
