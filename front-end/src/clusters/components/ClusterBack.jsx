import React, { useEffect, useState } from "react";
import axios from "axios";
import ClusterView from "./ClusterView";

const ClusterBack = () => {
  const [clusterData, setClusterData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [rangeValue, setRangeValue] = useState(40); // State for the range input

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

  const clusterCount = clusterData.length;

  useEffect(() => {
    fetchClusterData();
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="container mx-auto p-4">
      <div className="flex flex-row justify-between items-center mb-4">
        <p className="py-2 px-6 rounded-full border-2">
          Cluster Count: {clusterCount !== null ? clusterCount : "Loading..."}
        </p>

        <p className="py-2 px-6 rounded-full border-2 bg-purple-600 text-white bg-purple">
          Optimal Silhouette Score: {/* Update this with actual silhouette score if available */}
          {clusterCount !== null ? clusterCount : "Loading..."}
        </p>
      </div>

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

        <input
          type="range"
          min={0}
          max="100"
          value={rangeValue} // Controlled input
          onChange={(e) => setRangeValue(e.target.value)} // Update state on change
          className="range max-w-80"
        />
      </div>

      {error && <p className="text-red-600">{error}</p>}

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
