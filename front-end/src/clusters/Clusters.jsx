import React, { useEffect, useState } from "react";
import axios from "axios";
import ClusterView from "./components/ClusterView"; // Assuming this component renders individual cluster details

const Clusters = () => {
  const [clusterData, setClusterData] = useState([]);
  const [modelAccuracy, setModelAccuracy] = useState();
  const [silhouetteScore, setSilhouetteScore] = useState(0.8); // Default silhouette score
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch cluster data with the silhouette score
  const fetchClusterData = async (score) => {
    try {
      setLoading(true); // Set loading to true when fetching starts
      const response = await axios.get(
        `http://localhost:5000/api/get-clusters?score=${score}`
      );
      setClusterData(response.data);
      setLoading(false); // Set loading to false when fetch completes
    } catch (err) {
      setError("Error fetching cluster data");
      setLoading(false); // Set loading to false on error
    }
  };

  // Calculate cluster count based on clusterData length
  const clusterCount = clusterData.length;

  // Fetch data when the component mounts
  useEffect(() => {
    fetchClusterData(silhouetteScore);
  }, []);

  const [isTraining, setIsTraining] = useState(false);
  const [statusMessage, setStatusMessage] = useState("");

  // Function to start the training
  const startTraining = async () => {
    setStatusMessage("Model is training...");
    setIsTraining(true);

    try {
      const response = await fetch(
        "http://localhost:5000/api/train-xai-model",
        { method: "GET" }
      );
      const data = await response.json();
      console.log("Model Accuracy : " + data.accuracy);

      if (data.accuracy) {
        // Round model accuracy to 4 decimal places
        const roundedAccuracy = data.accuracy.toFixed(4);
        setModelAccuracy(roundedAccuracy);
      }

      if (!response.ok) {
        throw new Error("Error starting model training");
      }

      const intervalId = setInterval(async () => {
        const statusResponse = await fetch(
          "http://localhost:5000/api/training-status",
          { method: "GET" }
        );
        const status = await statusResponse.json();

        if (!status.is_training) {
          setStatusMessage(
            `Training complete!\nModel Accuracy: ${data.accuracy.toFixed(4)}`
          );
          setIsTraining(false);
          clearInterval(intervalId);
        }
      }, 2000);
    } catch (error) {
      console.error("Error during training:", error);
      setStatusMessage("An error occurred during training.");
      setIsTraining(false);
    }
  };

  return (
    <div className="container mx-auto p-4">
      {/* Header */}
      <div className="flex flex-row justify-between items-center mb-4">
        <p className="py-2 px-6 rounded-full border-2">
          Cluster Count: {clusterCount !== null ? clusterCount : "Loading..."}
        </p>

        {/* model traing button */}
        <div className=" flex gap-2 items-center bg-lightPurple p-2 rounded-full">
          <button
            onClick={startTraining}
            disabled={isTraining}
            className="py-2 px-6 rounded-full border-2  text-white bg-darkPurple"
          >
            {isTraining ? "Training in Progress..." : "Start Training"}
          </button>

          {/* Status message */}
          <p className=" text-red-500 mr-3">{statusMessage}</p>
        </div>

        <p className="py-2 px-6 rounded-full border-2  text-white bg-purple">
          Optimal Silhouette Score: 0.80
        </p>
      </div>

      {/* Silhouette Score changing */}
      <div className="flex flex-col items-center justify-center gap-2 pt-4">
        <div className="flex gap-2">
          <p className="py-2 px-6 rounded-full border-2">
            Silhouette Score: {silhouetteScore}
          </p>

          <button
            className="hover:scale-105 px-6 py-2 rounded-full hover:bg-purple-40 transition-all cursor-pointer text-white bg-purple"
            onClick={() => fetchClusterData(silhouetteScore)}
          >
            Apply
          </button>
        </div>

        {/* Range bar */}
        <input
          type="range"
          min="0"
          max="1"
          step="0.01"
          value={silhouetteScore}
          onChange={(e) => setSilhouetteScore(e.target.value)} // Update silhouette score
          className="range max-w-80"
        />
      </div>

      {/* Error handling */}
      {error && <p className="text-red-600">{error}</p>}

      {/* Loading Message */}
      {loading && <p>Please wait.</p>}

      {/* Clusters */}
      <div className="py-5">
        {loading ? (
          <p className=" font-bold text-red-500">Loading results...</p>
        ) : (
          <div className="grid grid-cols-5 gap-4">
            {clusterData.map((cluster, index) => (
              <div
                key={index}
                className="p-4 border rounded-full text-center hover:scale-105 cursor-pointer transition-all"
              >
                <ClusterView
                  clusterName={cluster.cluster}
                  numOfPatterns={cluster.pattern_count}
                  numOfAlerts={cluster.total_alerts}
                />
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Clusters;
