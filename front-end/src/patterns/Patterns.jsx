import React, { useEffect, useState } from "react";
import axios from "axios";
import AlertTable from "../alerts/components/AlertTable";

const Patterns = () => {
  // State to store pattern count and pattern data
  const [patternCount, setPatternCount] = useState(0);
  const [patternData, setPatternData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // For search functionality
  const [selectedFeature, setSelectedFeature] = useState("");
  const [searchValue, setSearchValue] = useState("");
  const [filteredData, setFilteredData] = useState([]);

  

  // Fetch pattern data from backend when the component mounts
  useEffect(() => {
    const fetchPatternData = async () => {
      try {
        const response = await axios.get(
          "http://localhost:5000/api/get_patterns"
        );
        const { pattern_count, pattern_data } = response.data;

        // Set pattern count and pattern data
        setPatternCount(pattern_count);
        setPatternData(pattern_data);
        setFilteredData(pattern_data);
        setLoading(false);
      } catch (err) {
        setError("Error fetching pattern data");
        setLoading(false);
      }
    };

    //defualt filtered data
    const setDefaultFilteredData =() => {
      // setFilteredData(patternData);

    };

    fetchPatternData();
    setDefaultFilteredData();
  }, []);


  // Handle search operation
  const handleSearch = () => {
    if (selectedFeature && searchValue) {
      // Filter rows based on the selected feature and search value
      const filtered = patternData.filter((row) =>
        row[selectedFeature]?.toString().toLowerCase().includes(searchValue.toLowerCase())
      );
      setFilteredData(filtered);
    } else {
      setFilteredData(patternData); // Show all rows if no search criteria
    }
  };

 


  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div>
      {/* Header */}
      <div className=" flex flex-row justify-between items-center">
        <p className="py-2 px-6 rounded-full border-2">
          Pattern Count: {patternCount !== null ? patternCount : "Loading..."}
        </p>
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
          {patternData.length > 0 &&
            Object.keys(patternData[0]).map((key) => (
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

export default Patterns;
