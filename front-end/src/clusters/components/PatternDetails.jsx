import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom"; // Import useNavigate
import axios from "axios";
import AlertTable from "../../alerts/components/AlertTable";
import { IoArrowBack } from "react-icons/io5";

const PatternDetails = () => {
  const { clusterName } = useParams(); // Get clusterName from URL
  const navigate = useNavigate(); // Initialize useNavigate
  const [patternData, setPatternData] = useState([]);
  const [clusterNumber, setClusterNumber] = useState();
  const [patternCount, setPatternCount] = useState(0);
  const [alertCount, setAlertCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch pattern data for the specific cluster
  const fetchClusterPatterns = async () => {
    try {
      const response = await axios.get(
        `http://localhost:5000/api/cluster/${clusterName}/patterns`
      );
      const { alert_count, cluster_name, pattern_count, pattern_data } =
        response.data;
      setPatternData(pattern_data);
      setClusterNumber(cluster_name);
      setPatternCount(pattern_count);
      setAlertCount(alert_count);
      setLoading(false);
    } catch (err) {
      setError("Error fetching cluster patterns");
      setLoading(false);
    }
  };

  // Fetch the data when the component mounts
  useEffect(() => {
    fetchClusterPatterns();
  }, [clusterName]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="container mx-auto p-4">
      <button
        className="mb-4 text-blue-500 hover:underline border px-4 py-2 rounded-full flex items-center justify-center gap-2"
        onClick={() => navigate("/clusters-back")} // Navigate to /clusters-back
      >
        <div>
          <IoArrowBack />
        </div>
        Back
      </button>
      <h2 className="text-2xl font-bold mb-4 bg-lightPurple rounded-full px-4 py-2 flex">
        Patterns for Cluster - {clusterName}
      </h2>
      <p>Pattern Count : <span className=" font-bold">{patternCount}</span></p>
      <p>Alert Count   : <span className=" font-bold">{alertCount}</span></p>

      {/* List the pattern details */}
      <AlertTable csvAlertData={patternData} />
    </div>
  );
};

export default PatternDetails;
