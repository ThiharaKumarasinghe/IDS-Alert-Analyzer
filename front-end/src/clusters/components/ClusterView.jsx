import { useNavigate } from "react-router-dom";

const ClusterView = ({ clusterName, numOfPatterns, numOfAlerts }) => {
  const navigate = useNavigate();

  const handleInspectPatterns = () => {
    // Navigate to the pattern details page for the selected cluster
    navigate(`/cluster/${clusterName}/patterns`);
  };

  const handleViewExplanation = () => {
    // Navigate to the pattern details page for the selected cluster
    console.log("View Explanation")
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

      <button
        className="mt-2 mb-4 bg-purple text-white px-4 py-2 rounded-lg hover:bg-darkPurple"
        onClick={handleViewExplanation}
      >
        View Explanation
      </button>

      
    </div>
  );
};

export default ClusterView;
