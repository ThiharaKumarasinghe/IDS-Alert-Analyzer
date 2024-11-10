import { useNavigate } from "react-router-dom";
import ExplanationModel from "./ExplanationXAI";
import React, { useState } from "react";

const ClusterView = ({
  clusterName,
  numOfPatterns,
  numOfAlerts,
  isModelTraining,
}) => {
  const navigate = useNavigate();

  const handleInspectPatterns = () => {
    // Navigate to the pattern details page for the selected cluster
    navigate(`/cluster/${clusterName}/patterns`);
  };

  const handleExplanationView = () => {
    // Navigate to the pattern details page for the selected cluster
    navigate(`/cluster/${clusterName}/xai`);
  };

  return (
    <div className="border rounded-full p-4 flex flex-col justify-center items-center bg-lightPurple">
      <h3 className="text-lg font-bold">{clusterName}</h3>
      <p className="text-sm">Patterns: {numOfPatterns}</p>
      <p className="text-sm">Alerts: {numOfAlerts}</p>

      <button
        className="mt-2 bg-purple text-white px-4 py-2 rounded-lg hover:bg-darkPurple"
        onClick={handleInspectPatterns}
      >
        Inspect Patterns
      </button>

      {(isModelTraining ||
        window.location.href === "http://localhost:5173/clusters-back") && (
        <button
          className="mt-2 bg-purple text-white px-4 py-2 rounded-lg hover:bg-darkPurple mb-4"
          onClick={handleExplanationView}
        >
          View Explanation
        </button>
      )}
    </div>
  );
};

export default ClusterView;
