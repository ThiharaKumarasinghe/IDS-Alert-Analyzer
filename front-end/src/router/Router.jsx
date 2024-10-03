import {
    createBrowserRouter,
  } from "react-router-dom";
import Patterns from "../patterns/Patterns";
import Home from "../Home";
import Alerts from "../alerts/Alerts";
import Clusters from "../clusters/Clusters";
import XAI from "../XAI/XAI";

  const router = createBrowserRouter([
    {
      path: "/",
      element:<Home/>,
      children: [
        {
            path: "/",
            element:<Alerts/>,
        },
        {
            path: "/patterns",
            element:<Patterns/>,
        },
        {
            path: "/clusters",
            element:<Clusters/>,
        },
        {
            path: "/xai",
            element:<XAI/>,
        },

      ]
    },
  ]);

  export default router;