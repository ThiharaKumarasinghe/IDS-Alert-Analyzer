import React, { useEffect, useState } from "react";
import AlertTable from "./components/AlertTable";

const Alerts = () => {
  const [alertCount, setAlertCount] = useState(null);
  const [csvAlertData, setCsvAlertData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // For search functionality
  const [selectedFeature, setSelectedFeature] = useState("");
  const [searchValue, setSearchValue] = useState("");
  const [filteredData, setFilteredData] = useState([]);

  // Fetch the alert count from the Flask backend
  const fetchAlertCount = async () => {
    try {
      const response = await fetch("http://localhost:5000/api/alert-count");
      const data = await response.json();
      setAlertCount(data.alertCount);
    } catch (error) {
      console.error("Error fetching alert count:", error);
    }
  };

  // Fetch all alert data from Flask backend
  const fetchAllAlertData = async () => {
    fetch("http://localhost:5000/api/csv-data-alert")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        setCsvAlertData(data);
        setFilteredData(data); // Initialize filtered data to show all data initially
        setLoading(false);
      })
      .catch((error) => {
        setError(error);
        setLoading(false);
      });
  };

  // Handle search operation
  const handleSearch = () => {
    if (selectedFeature && searchValue) {
      // Filter rows based on the selected feature and search value
      const filtered = csvAlertData.filter((row) =>
        row[selectedFeature]?.toString().toLowerCase().includes(searchValue.toLowerCase())
      );
      setFilteredData(filtered);
    } else {
      setFilteredData(csvAlertData); // Show all rows if no search criteria
    }
  };


// Function to download the CSV file
const handleDownloadCsv = () => {
  const link = document.createElement('a');
  link.href = "http://localhost:5000/api/download-csv";  // This endpoint serves the CSV file
  link.setAttribute('download', 'alert-data.csv'); // Name of the downloaded file
  document.body.appendChild(link); // Append link to the body
  link.click(); // Programmatically click the link to trigger download
  document.body.removeChild(link); // Remove link from the body after download
};

  useEffect(() => {
    fetchAlertCount();
    fetchAllAlertData();
  }, []);

  if (loading) {
    return <p>Loading... Please wait!</p>;
  }

  if (error) {
    return <p>Error: {error.message}</p>;
  }

  return (
    <div>
      {/* Header */}
      <div className=" flex flex-row justify-between items-center">
        <p className="py-2 px-6 rounded-full border-2">
          Alert Count: {alertCount !== null ? alertCount : "Loading..."}
        </p>

        <button className=" bg-darkPurple text-white px-6 py-2 rounded-full hover:bg-lightPurple hover:text-black transition-all cursor-pointer" onClick={handleDownloadCsv}>
          Open CSV File
        </button>
      </div>

      {/* Search bar */}
      <div className=" bg-lightPurple rounded-full mt-3 py-4 px-10 flex flex-row items-center justify-center gap-4">
        {/* Select the option */}
        <select
          className="select select-bordered w-full max-w-xs"
          onChange={(e) => setSelectedFeature(e.target.value)}
        >
          <option disabled selected>
            Select Required Feature
          </option>
          {csvAlertData.length > 0 &&
            Object.keys(csvAlertData[0]).map((key) => (
              <option key={key} value={key}>
                {key}
              </option>
            ))}
        </select>

        {/* Enter the value */}
        <input
          type="text"
          placeholder="Type Value"
          className="input input-bordered w-full max-w-xs"
          value={searchValue}
          onChange={(e) => setSearchValue(e.target.value)}
        />

        {/* Search button */}
        <button
          className=" bg-darkPurple text-white px-6 py-2 rounded-full hover:bg-purple hover:text-black transition-all cursor-pointer"
          onClick={handleSearch}
        >
          Search
        </button>
      </div>

      {/* Alert data */}
      <AlertTable csvAlertData={filteredData} />
    </div>
  );
};

export default Alerts;
