import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.smartdrone.app',
  appName: 'SmartDrone',
  webDir: 'www',
  // Live-reload from your Render deployment
  server: {
    url: 'https://smartdrone.onrender.com',
    cleartext: false,
  },
  ios: {
    contentInset: 'always',
    backgroundColor: '#0a0608',
    scrollEnabled: true,
  },
  android: {
    backgroundColor: '#0a0608',
    allowMixedContent: false,
  },
  plugins: {
    SplashScreen: {
      launchShowDuration: 2500,
      launchAutoHide: true,
      backgroundColor: '#0a0608',
      showSpinner: false,
      spinnerColor: '#c9a84c',
    },
    StatusBar: {
      style: 'Dark',
      backgroundColor: '#0a0608',
    },
  },
};

export default config;
