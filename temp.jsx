import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { IoArrowBack } from "react-icons/io5";

const ExplanationXAI = () => {
  const { clusterName } = useParams(); // Get clusterName from URL
  const navigate = useNavigate(); // Initialize useNavigate
  const [clusterResult, setClusterResult] = useState(null); // Initialize with null
  const [loading, setLoading] = useState(true); // Set loading to true initially
  const [error, setError] = useState(null); // Error state
  const [statusMessage, setStatusMessage] = useState(""); // Status message

  // Function to fetch aggregate explanations for a cluster
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
      setLoading(false); // Set loading to false after fetching
      setStatusMessage("Explanations fetched successfully");
    } catch (error) {
      console.error("Error fetching explanations:", error);
      setError("An error occurred while fetching explanations.");
      setLoading(false); // Set loading to false even on error
    }
  };

  // Fetch the data when the component mounts or when clusterName changes
  useEffect(() => {
    getClusterExplanations(clusterName);
  }, [clusterName]);

  // Handle loading and error states
  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="container mx-auto p-4">
      {/* Back button */}
      <button
        className="mb-4 text-blue-500 hover:underline border px-4 py-2 rounded-full flex items-center justify-center gap-2"
        onClick={() => navigate("/clusters-back")} // Navigate to /clusters-back
      >
        <div>
          <IoArrowBack />
        </div>
        Back
      </button>

      {/* Cluster explanations */}
      <h2 className="text-2xl font-bold mb-4 bg-lightPurple rounded-full px-4 py-2 flex">
        Explanation for Cluster - {clusterName}
      </h2>

      {/* Display fetched explanations */}
      <div>
        {clusterResult ? (
          <pre>{JSON.stringify(clusterResult, null, 2)}</pre> // Pretty print the fetched data
        ) : (
          <p>No data available for this cluster</p>
        )}
      </div>

      {/* Status message */}
      {statusMessage && <p>{statusMessage}</p>}
    </div>
  );
};

export default ExplanationXAI;
