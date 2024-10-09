import React, { useEffect, useState } from "react";
import axios from "axios";
import ClusterView from "./ClusterView";
import { useNavigate } from "react-router-dom";

const ClusterBack = () => {
    const navigate = useNavigate();

  const handleBackToCluster = () => {
    // Navigate to the cluster page
    navigate(`/clusters`);
  };

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

        <button
        className="mt-2 mb-4 bg-purple text-white px-4 py-2 rounded-lg hover:bg-darkPurple"
        onClick={handleBackToCluster}
      >
        Press to Change Silhouette Score
      </button>
      </div>

      

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
