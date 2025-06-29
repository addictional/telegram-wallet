import React from "react";
import {createBrowserRouter,RouterProvider,} from 'react-router'
import Cards from '@/pages/Cards'
import Wallet from '@/pages/Wallet'

const router = createBrowserRouter([
  {
    path: "/",
    element: <Cards/>,
  },
  {
    path: "/wallet/:id",
    element: <Wallet/>,
  },
]);

function App() {

  // const sendData = () => {
  //   if (window.Telegram.WebApp) {
  //     window.Telegram.WebApp.sendData("👋 Привет из React!");
  //   }
  // };

  React.useEffect(() => {
    if (window.Telegram.WebApp) {
      window.Telegram.WebApp.ready();
    }
  }, []);

  return (
    <RouterProvider router={router} />
  );
}

export default App;




