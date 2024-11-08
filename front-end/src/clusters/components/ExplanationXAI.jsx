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

  // Parse the explanation text to a structured format
  const parseExplanation = (explanationText) => {
    const lines = explanationText.split("\n");
    let parsed = [];
    let currentSection = null;

    lines.forEach((line) => {
      if (line.startsWith("**") && line.endsWith(":**")) {
        // Create a new section with the heading
        currentSection = {
          heading: line.replace(/\*\*/g, "").replace(":", ""),
          items: [],
        };
        parsed.push(currentSection);
      } else if (line.startsWith("*")) {
        if (currentSection) {
          const itemParts = line.split(":");
          if (itemParts.length > 1) {
            currentSection.items.push({
              feature: itemParts[0].replace("* ", "").trim(),
              description: itemParts[1].trim(),
            });
          }
        }
      }
    });
    return parsed;
  };

  // Function to fetch and display explanation details
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
    ? Object.entries(clusterResult).sort((a, b) => b[1] - a[1])
    : [];

  // Prepare data for the chart
  const chartData = {
    labels: sortedClusterResult.map((item) => item[0]), // Feature names
    datasets: [
      {
        label: "LIME Explanation Values",
        data: sortedClusterResult.map((item) => item[1]), // Explanation values
        backgroundColor: sortedClusterResult.map(
          (_, idx) => `hsl(${(idx * 35) % 360}, 70%, 50%)`
        ), // Dynamic colors
        borderWidth: 2,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    indexAxis: "y",
    plugins: {
      legend: {
        position: "top",
        labels: {
          color: "#333",
          font: { size: 14 },
        },
      },
      title: {
        display: true,
        text: `LIME Explanations for Cluster ${clusterName}`,
        font: { size: 20 },
        color: "#111",
      },
      tooltip: {
        backgroundColor: "rgba(0,0,0,0.7)",
        titleColor: "#fff",
        bodyColor: "#fff",
      },
    },
    scales: {
      y: { ticks: { color: "#333", autoSkip: false }, grid: { display: false } },
      x: { beginAtZero: true, grid: { color: "rgba(200,200,200,0.3)" } },
    },
    animation: { duration: 2000, easing: "easeInOutBounce" },
  };

  // Component to display explanations in a structured format
  const ExplanationDisplay = ({ explanation }) => {
    const parsedExplanation = parseExplanation(explanation);

    return (
      <div className="mt-4 p-4 bg-lightGray rounded-lg shadow-lg max-w-full overflow-x-auto">
        {parsedExplanation.map((section, index) => (
          <div key={index} className="mb-6">
            <h4 className="text-lg font-semibold mb-2">{section.heading}</h4>
            <ul className="list-disc pl-6 space-y-2">
              {section.items.map((item, idx) => (
                <li key={idx}>
                  <span className="font-semibold">{item.feature}:</span> {item.description}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="container mx-auto p-4">
      {/* Back button */}
      <button
        className="mb-4 text-blue-500 hover:underline border px-4 py-2 rounded-full flex items-center justify-center gap-2"
        onClick={() => navigate("/clusters-back")}
      >
        <IoArrowBack />
        Back
      </button>

      {/* Cluster explanations */}
      <h2 className="text-2xl font-bold mb-4 bg-lightPurple rounded-full px-4 py-2 flex">
        Explanation for Cluster - {clusterName}
      </h2>

      {/* Display fetched explanations */}
      <div>
        {clusterResult ? (
          <Bar data={chartData} options={chartOptions} />
        ) : (
          <p>No data available for this cluster</p>
        )}
      </div>

      {/* Status message */}
      {statusMessage && <p className=" text-purple text-sm">{statusMessage}</p>}

      <div className="max-w-full p-4">
        {/* Gemini explanation */}
        {clusterResult && (
          <button
            onClick={() => explainCluster(clusterResult)}
            className="bg-darkPurple text-white p-4 rounded-2xl mt-4 hover:scale-105 transition-transform duration-300"
          >
            Explain This Result
          </button>
        )}

        {/* Display explanation */}
        {explanation && <ExplanationDisplay explanation={explanation} />}
      </div>
    </div>
  );
};

export default ExplanationXAI;
