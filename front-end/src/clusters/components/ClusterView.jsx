import React from "react";

const ClusterView = ({ clusterName, numOfPatterns, numOfAlerts }) => {
  return (
    <div className="border rounded-full p-4 flex flex-col justify-center items-center bg-lightPurple">
      <h3 className="text-lg font-bold">{clusterName}</h3>
      <p className="text-sm">Patterns : {numOfPatterns}</p>
      <p className="text-sm">Alerts : {numOfAlerts}</p>

      
      <button className="mt-4 bg-purple text-white px-2 py-2 rounded-lg hover:bg-darkPurple">
        View Explanation
      </button>

      <button className="mt-2 mb-4 bg-purple text-white px-4 py-2 rounded-lg hover:bg-darkPurple">
        Inspect Patterns
      </button>

    </div>
  );
};

export default ClusterView;
