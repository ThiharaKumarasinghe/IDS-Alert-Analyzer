import {
    createBrowserRouter,
  } from "react-router-dom";
import Patterns from "../patterns/Patterns";
import Home from "../Home";
import Alerts from "../alerts/Alerts";
import Clusters from "../clusters/Clusters";
import XAI from "../XAI/XAI";
import PatternDetails from "../clusters/components/PatternDetails";
import ClusterBack from "../clusters/components/ClusterBack";

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
            path: "/cluster/:clusterName/patterns",
            element:<PatternDetails/>,
        },
        {
          path: "/clusters-back",
          element:<ClusterBack/>,
      },
        {
          path: "/xai",
          element:<XAI/>,
      },

      ]
    },
  ]);

  export default router;