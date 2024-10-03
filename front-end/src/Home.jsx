import React from "react";
import { Outlet } from "react-router-dom";
import SideBar from "./components/SideBar";

const Home = () => {
  return (
    <div>
      <SideBar />
      <div className=" ml-40 p-10">
        <Outlet />
      </div>
    </div>
  );
};

export default Home;
