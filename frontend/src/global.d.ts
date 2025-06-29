// src/global.d.ts

interface TelegramWebApp {
  initData: string;
  initDataUnsafe: unknown;
  sendData: (data: string) => void;
  close: () => void;
  expand: () => void;
  ready: () => void;
  version: string;
  platform: string;
  themeParams: unknown;
  colorScheme: string;
  isExpanded: boolean;
  isDarkMode: boolean;
}

interface Window {
  Telegram: {
    WebApp: TelegramWebApp;
  };
}


declare module '*.svg?react' {
  import * as React from 'react';
  const Component: React.FC<React.SVGProps<SVGSVGElement>>;
  export default Component;
}