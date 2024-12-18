import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { IoArrowBack } from "react-icons/io5";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import ClipLoader from "react-spinners/ClipLoader"; // Importing loading spinner

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const ExplanationXAI = () => {
  const { clusterName } = useParams(); // Get clusterName from URL
  const navigate = useNavigate(); // Initialize useNavigate
  const [clusterResult, setClusterResult] = useState(null); // Initialize with null
  const [loading, setLoading] = useState(true); // Set loading to true initially
  const [error, setError] = useState(null); // Error state
  const [statusMessage, setStatusMessage] = useState(""); // Status message
  const [explanation, setExplanation] = useState(null);

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
  if (loading)
    return (
      <div className="flex justify-center items-center h-screen">
        <ClipLoader color="#36D7B7" size={50} /> {/* Loading spinner */}
      </div>
    );
  if (error) return <p>{error}</p>;

  // Sort the cluster result by values in descending order
  const sortedClusterResult = clusterResult
    ? Object.entries(clusterResult).sort((a, b) => b[1] - a[1]) // Sort in descending order
    : [];

  // Create reversed arrays for labels and values
  const sortedLabels = sortedClusterResult.map((item) => item[0]); // Sorted feature names
  const sortedValues = sortedClusterResult.map((item) => item[1]); // Sorted explanation values

  // Generate a colorful array of background colors for the bars
  const backgroundColors = sortedValues.map(
    (_, idx) => `hsl(${(idx * 35) % 360}, 70%, 50%)` // Generate dynamic colors using HSL
  );

  // Prepare data for the chart
  const chartData = {
    labels: sortedLabels, // Feature names
    datasets: [
      {
        label: "LIME Explanation Values",
        data: sortedValues, // Explanation values
        backgroundColor: backgroundColors, // Colorful bars
        borderColor: backgroundColors, // Matching border color
        borderWidth: 2,
        hoverBackgroundColor: "rgba(255, 99, 132, 0.2)", // Hover effect
        hoverBorderColor: "rgba(255, 99, 132, 1)", // Hover effect border
        barThickness: 30, // Thicker bars for visibility
        barPercentage: 0.5, // Space between bars
        categoryPercentage: 0.5, // Space between categories
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    indexAxis: "y", // Keep horizontal bar chart
    plugins: {
      legend: {
        position: "top",
        labels: {
          color: "#333", // Legend color
          font: {
            size: 14, // Slightly larger font for legend
          },
        },
      },
      title: {
        display: true,
        text: `LIME Explanations for Cluster ${clusterName}`,
        font: {
          size: 20, // Larger title font size
        },
        color: "#111",
      },
      tooltip: {
        backgroundColor: "rgba(0,0,0,0.7)", // Tooltip customization
        titleColor: "#fff",
        bodyColor: "#fff",
        borderWidth: 1,
        borderColor: "#333",
      },
    },
    scales: {
      y: {
        ticks: {
          color: "#333", // Y-axis (features) label color
          font: {
            size: 12, // Adjusted label size for better readability
          },
          autoSkip: false, // Prevent skipping of labels
        },
        grid: {
          display: false, // Remove Y-axis grid for cleaner look
        },
      },
      x: {
        beginAtZero: true,
        min: Math.max(...sortedValues), // Max value from sortedValues
        max: Math.min(...sortedValues), // Min value from sortedValues
        ticks: {
          color: "#333", // X-axis label color
          font: {
            size: 12, // Adjusted X-axis font size
          },
        },
        grid: {
          color: "rgba(200,200,200,0.3)", // Light X-axis grid
        },
      },
    },
    animation: {
      duration: 2000, // Animation duration for bar loading
      easing: "easeInOutBounce", // Smooth animation effect
    },
  };

  // Function to explain the cluster result
  const explainCluster = async (clusterResult) => {
    console.log(clusterResult);
    setStatusMessage("Fetching explanation...");

    try {
      const response = await fetch(
        "http://localhost:5000/api/explain-cluster",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ cluster_result: clusterResult }),
        }
      );

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
          <div>
            <Bar data={chartData} options={chartOptions} />
          </div>
        ) : (
          <p>No data available for this cluster</p>
        )}
      </div>

      {/* Status message */}
      {statusMessage && <p className=" text-purple text-sm">{statusMessage}</p>}

      <div className="max-w-full p-4">
        {/* Gemini explanation */}
        {clusterResult ? (
          <button
            onClick={() => explainCluster(clusterResult)} // Directly pass clusterResult
            className="bg-darkPurple text-white p-4 rounded-2xl mt-4 hover:scale-105 transition-transform duration-300"
          >
            Explain This Result
          </button>
        ) : (
          ""
        )}

        {/* Display explanation */}
        {explanation && (
          <div className="mt-4 p-4 bg-lightGray rounded-lg shadow-lg max-w-full overflow-x-auto">
            <pre className="whitespace-pre-wrap break-words">{explanation}</pre>
          </div>
        )}
      </div>
    </div>
  );
};

export default ExplanationXAI;
