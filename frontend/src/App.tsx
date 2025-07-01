import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router";
import Cards from "@/pages/Cards";
import Wallet from "@/pages/Wallet";
import { useLogin } from "./hooks/useLogin";
import {
  retrieveLaunchParams,
  init,
  initData,
  isTMA,
  viewport,
} from "@telegram-apps/sdk";

const noInsets = {
  left: 0,
  top: 0,
  bottom: 0,
  right: 0,
} as const;
const themeParams = {
  accent_text_color: "#6ab2f2",
  bg_color: "#17212b",
  button_color: "#5288c1",
  button_text_color: "#ffffff",
  destructive_text_color: "#ec3942",
  header_bg_color: "#17212b",
  hint_color: "#708499",
  link_color: "#6ab3f3",
  secondary_bg_color: "#232e3c",
  section_bg_color: "#17212b",
  section_header_text_color: "#6ab3f3",
  subtitle_text_color: "#708499",
  text_color: "#f5f5f5",
} as const;

// mockTelegramEnv({
//   launchParams: {
//     tgWebAppThemeParams: themeParams,
//     tgWebAppData: new URLSearchParams([
//       [
//         "user",
//         JSON.stringify({
//           id: 1,
//           first_name: "Pavel",
//         }),
//       ],
//       ["hash", ""],
//       ["signature", ""],
//       ["auth_date", Date.now().toString()],
//     ]),
//     tgWebAppStartParam: "debug",
//     tgWebAppVersion: "8",
//     tgWebAppPlatform: "tdesktop",
//   },
//   onEvent(e) {
//     if (e[0] === "web_app_request_theme") {
//       return emitEvent("theme_changed", { theme_params: themeParams });
//     }
//     if (e[0] === "web_app_request_viewport") {
//       return emitEvent("viewport_changed", {
//         height: window.innerHeight,
//         width: window.innerWidth,
//         is_expanded: true,
//         is_state_stable: true,
//       });
//     }
//     if (e[0] === "web_app_request_content_safe_area") {
//       return emitEvent("content_safe_area_changed", noInsets);
//     }
//     if (e[0] === "web_app_request_safe_area") {
//       return emitEvent("safe_area_changed", noInsets);
//     }
//   },
// });

const router = createBrowserRouter([
  {
    path: "/",
    element: <Cards />,
  },
  {
    path: "/wallet/:id",
    element: <Wallet />,
  },
]);

function App() {
  const { login, isAuthorized } = useLogin();

  React.useEffect(() => {
    if (isTMA()) {
      console.log("It's Telegram Mini Apps");
    }
    init();
    initData.restore();
    login(initData.raw()!);

    if (viewport.expand.isAvailable()) {
      viewport.expand();
    }
  }, []);

  if (!isAuthorized) {
    return <span>loading</span>;
  }

  return <RouterProvider router={router} />;
}

export default App;
