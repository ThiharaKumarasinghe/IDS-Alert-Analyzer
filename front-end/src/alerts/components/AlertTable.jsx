import React, { useState } from "react";

const AlertTable = ({ csvAlertData }) => {
  // State to track selected columns
  const [selectedColumns, setSelectedColumns] = useState(
    csvAlertData.length > 0 ? Object.keys(csvAlertData[0]) : []
  );
  // State to handle dropdown visibility
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  // Toggle the dropdown visibility
  const toggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  // Handle checkbox change for column selection
  const handleCheckboxChange = (event) => {
    const { value, checked } = event.target;
    if (checked) {
      setSelectedColumns([...selectedColumns, value]);
    } else {
      setSelectedColumns(selectedColumns.filter((col) => col !== value));
    }
  };

  return (
    <div className="mt-6 overflow-x-auto">
      {/* Dropdown to select columns */}
      <div className="flex justify-end mb-4 relative">
        <button
          className=" bg-purple hover:scale-105  text-white px-4 py-2 rounded-full text-sm font-semibold mr-3 mt-2"
          onClick={toggleDropdown}
        >
          Select Columns
        </button>

        {/* Dropdown Menu - Show/Hide based on state */}
        {isDropdownOpen && (
          <div className="absolute right-0 top-8 mt-5 w-48 bg-white border border-darkPurple rounded shadow-lg z-10">
            {csvAlertData.length > 0 &&
              Object.keys(csvAlertData[0]).map((key) => (
                <div key={key} className="flex items-center p-2">
                  <input
                    type="checkbox"
                    id={key}
                    value={key}
                    checked={selectedColumns.includes(key)}
                    onChange={handleCheckboxChange}
                    className="mr-2"
                  />
                  <label htmlFor={key} className="text-sm">
                    {key}
                  </label>
                </div>
              ))}
          </div>
        )}
      </div>

      {/* Table */}
      <table className="min-w-full border border-darkPurple">
        <thead className=" bg-darkPurple">
          <tr>
            {selectedColumns.map((key) => (
              <th
                key={key}
                className="px-4 py-3 text-center text-sm text-white font-bold border-b border-darkPurple"
              >
                {key}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {csvAlertData.map((row, index) => (
            <tr
              key={index}
              className={index % 2 === 0 ? "bg-white" : "bg-lightPurple"}
            >
              {selectedColumns.map((key, idx) => (
                <td
                  key={idx}
                  className="px-4 py-1 text-sm text-gray-700 border-b border-darkPurple"
                >
                  {row[key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AlertTable;
