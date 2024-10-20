import React from "react";
import { useLocation } from "react-router-dom"; // Import useLocation

const SideBar = () => {
  const location = useLocation(); // Get the current location

  return (
    <div className=" w-40 fixed z-30">
      <div className="flex h-screen flex-col justify-between border-e bg-lightPurple">
        <div className="px-4 py-6">
          <span className="grid h-10 w-32 place-content-center rounded-lg bg-purple text-xs text-white font-bold cursor-pointer">
            IDS Alerts Analyser
          </span>

          <ul className="mt-6 space-y-1">
          <li>
              <a
                href="/"
                className={`block rounded-lg px-4 py-2 text-sm font-medium hover:scale-105 transition-all ${
                  location.pathname === "/"
                    ? "bg-purple text-white"
                    : "text-gray-600 hover:bg-gray-100 hover:text-gray-700"
                }`}
              >
                Upload PACP
              </a>
            </li>
            <li>
              <a
                href="/alerts"
                className={`block rounded-lg px-4 py-2 text-sm font-medium hover:scale-105 transition-all ${
                  location.pathname === "/alerts"
                    ? "bg-purple text-white"
                    : "text-gray-600 hover:bg-gray-100 hover:text-gray-700"
                }`}
              >
                Alerts
              </a>
            </li>

            <li>
              <a
                href="/patterns"
                className={`block rounded-lg px-4 py-2 text-sm font-medium hover:scale-105 transition-all ${
                  location.pathname === "/patterns"
                    ? "bg-purple text-white"
                    : "text-gray-600 hover:bg-gray-100 hover:text-gray-700"
                }`}
              >
                Patterns
              </a>
            </li>

            <li>
              <a
                href="/clusters"
                className={`block rounded-lg px-4 py-2 text-sm font-medium hover:scale-105 transition-all ${
                  location.pathname === "/clusters"
                    ? "bg-purple text-white"
                    : "text-gray-600 hover:bg-gray-100 hover:text-gray-700"
                }`}
              >
                Clusters
              </a>
            </li>

            <li>
              <a
                href="/xai"
                className={`block rounded-lg px-4 py-2 text-sm font-medium hover:scale-105 transition-all ${
                  location.pathname === "/xai"
                    ? "bg-purple text-white"
                    : "text-gray-600 hover:bg-gray-100 hover:text-gray-700"
                }`}
              >
                XAI
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default SideBar;
