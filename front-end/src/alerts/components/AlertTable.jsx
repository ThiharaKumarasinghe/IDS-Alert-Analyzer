import React from "react";

const AlertTable = ({ csvAlertData }) => {
  return (
    <div className="mt-6 overflow-x-auto">
      <table className="min-w-full border border-darkPurple">
        <thead className=" bg-darkPurple">
          <tr>
            {csvAlertData.length > 0 &&
              Object.keys(csvAlertData[0]).map((key) => (
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
              {Object.values(row).map((value, idx) => (
                <td
                  key={idx}
                  className="px-4 py-1 text-sm text-gray-700 border-b border-darkPurple"
                >
                  {value}
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
