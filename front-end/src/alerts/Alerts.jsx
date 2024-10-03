import React, { useEffect, useState } from 'react'

const Alerts = () => {
  const [alertCount, setAlertCount]= useState(null);

  // Fetch the alert count from the Flask backend
  const fetchAlertCount = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/alert-count');
      const data = await response.json();
      console.log(data.alertCount);
      // Set the alert count to state
      setAlertCount(data.alertCount);
    } catch (error) {
      console.error("Error fetching alert count:", error);
    }
  };


  useEffect(() => {
    fetchAlertCount();
  }, []);


  
  return (
    <div>
      {/* Header */}
      <div className=' flex flex-row justify-between items-center'>
        <p className='py-2 px-6 rounded-full border-2'>Alert Count : {alertCount !== null ? alertCount : "Loading..."}</p>

        <button className=' bg-darkPurple text-white px-6 py-2 rounded-full hover:bg-lightPurple hover:text-black transition-all cursor-pointer'>Open CSV File</button>

      </div>

      {/* Search bar */}
      <div>
        Search bar
      </div>

      {/* Alert data */}
      <div>
        Alert data
      </div>

      


    </div>
  )
}

export default Alerts