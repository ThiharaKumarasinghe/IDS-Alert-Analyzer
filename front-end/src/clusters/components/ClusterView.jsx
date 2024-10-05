import React from 'react'

const ClusterView = ({ clusterName, numOfPatterns, numOfAlerts, onShowMore }) => {
  return (
<div className="flex justify-center items-center">
      {/* Circle */}
      <div className="w-64 h-64 rounded-full bg-lightPurple flex flex-col justify-center items-center text-center p-4 hover:scale-105 shadow-md">
        {/* Cluster Name */}
        <h2 className="text-xl font-bold mb-2">{clusterName}</h2>

        {/* Number of Patterns */}
        <p className="text-lg mb-2">Patterns: {numOfPatterns}</p>

        {/* Number of Alerts */}
        <p className="text-lg mb-4">Alerts: {numOfAlerts}</p>

        {/* Show More Button */}
        <button 
          className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-700" 
          onClick={onShowMore}>
          Show More
        </button>
      </div>
    </div>  )
}

export default ClusterView