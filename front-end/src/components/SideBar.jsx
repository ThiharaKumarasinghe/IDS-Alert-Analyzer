import React from "react";

const SideBar = () => {
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
                className="block rounded-lg px-4 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 hover:text-gray-700 hover:scale-105 transition-all"
              >
                Alerts
              </a>
            </li>

            <li>
              <a
                href="/patterns"
                className="block rounded-lg px-4 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 hover:text-gray-700 hover:scale-105 transition-all"              >
                Patterns
              </a>
            </li>

            <li>
              <a
                href="/clusters"
                className="block rounded-lg px-4 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 hover:text-gray-700 hover:scale-105 transition-all"              >
                Clusters
              </a>
            </li>

            <li>
              <a
                href="/xai"
                className="block rounded-lg px-4 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 hover:text-gray-700 hover:scale-105 transition-all"              >
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
