import React, { useState } from "react";
import ClusterView from "./components/ClusterView";

const Clusters = () => {
  const [custerCount, setClusterCount] = useState(5);

  const handdleSilhouette =()=> {
    print("Handdle");
  }

  return (
    <div>
      {/* Header */}
      <div className=" flex flex-row justify-between items-center">
        <p className="py-2 px-6 rounded-full border-2">
          Cluster Count: {custerCount !== null ? custerCount : "Loading..."}
        </p>

        <p className="py-2 px-6 rounded-full border-2 bg-purple text-white">
          Optimal Silhouette Score :{" "}
          {custerCount !== null ? custerCount : "Loading..."}
        </p>
      </div>

      {/* Silhouette Score changing */}
      <div className=" flex flex-col items-center justify-center gap-2 pt-4 ">
        <div className=" flex gap-2">
          <p className="py-2 px-6 rounded-full border-2">
            Silhouette Score :{" "}
            {custerCount !== null ? custerCount : "Loading..."}
          </p>

          <button
            className=" bg-darkPurple text-white px-6 py-2 rounded-full hover:bg-lightPurple hover:text-black transition-all cursor-pointer"
            onClick={handdleSilhouette}
          >
            Apply
          </button>
        </div>

        {/* Range bar */}
        <input
          type="range"
          min={0}
          max="100"
          value="40"
          className="range max-w-80"
        />
      </div>

      {/* Clusters */}
      <div className=" py-5">
        <ClusterView data={"ewrwe"} />
      </div>
    </div>
  );
};

export default Clusters;
