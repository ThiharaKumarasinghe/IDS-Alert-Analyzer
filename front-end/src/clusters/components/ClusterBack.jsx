import React, { useEffect, useState } from "react";
import axios from "axios";
import ClusterView from "./components/ClusterView"; // Assuming this component renders individual cluster details

const ClusterBack = () => {
  // State to store the fetched cluster data and loading/error status
  const [clusterData, setClusterData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch cluster data from the backend
  const fetchClusterData = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/get-clusters-back');
      setClusterData(response.data);
      setLoading(false);
    } catch (err) {
      setError('Error fetching cluster data');
      setLoading(false);
    }
  };

  // Calculate cluster count based on clusterData length
  const clusterCount = clusterData.length; // Use `.length` property, not a function

  // Fetch data when the component mounts
  useEffect(() => {
    fetchClusterData();
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="container mx-auto p-4">
      {/* Header */}
      <div className="flex flex-row justify-between items-center mb-4">
        <p className="py-2 px-6 rounded-full border-2">
          Cluster Count: {clusterCount !== null ? clusterCount : "Loading..."}
        </p>

        <p className="py-2 px-6 rounded-full border-2 bg-purple-600 text-white bg-purple">
          Optimal Silhouette Score: {/* Update this with actual silhouette score if available */}
          {clusterCount !== null ? clusterCount : "Loading..."}
        </p>
      </div>

      {/* Silhouette Score changing */}
      <div className="flex flex-col items-center justify-center gap-2 pt-4">
        <div className="flex gap-2">
          <p className="py-2 px-6 rounded-full border-2">
            Silhouette Score: {/* Placeholder or actual score if available */}
            {clusterCount !== null ? clusterCount : "Loading..."}
          </p>

          <button className="bg-purple-600 text-white px-6 py-2 rounded-full hover:bg-purple-400 hover:text-black transition-all cursor-pointer">
            Apply
          </button>
        </div>

        {/* Range bar */}
        <input
          type="range"
          min={0}
          max="100"
          value="40"
          className="range max-w-80"
        />
      </div>

      {/* Error handling */}
      {error && <p className="text-red-600">{error}</p>}

      {/* Clusters */}
      <div className="py-5">
        {loading ? (
          <p>Loading...</p>
        ) : (
          <div className="grid grid-cols-5 gap-4">
            {clusterData.map((cluster, index) => (
              <div key={index} className="p-4 border rounded-full text-center hover:scale-105 cursor-pointer transition-all">
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

export default ClusterBack;
