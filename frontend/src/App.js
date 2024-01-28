import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { ThemeProvider, StyledEngineProvider, createTheme } from '@mui/material/styles';
import { SnackbarProvider } from 'notistack';
import Auth from './components/Auth';
import CookiesNotification from './components/CookiesNotification';
import SettingsNotification from './components/SettingsNotification';
import GoogleAnalytics from './components/GoogleAnalytics';
import ScrollReset from './components/ScrollReset';
import useSettings from './hooks/useSettings';
import Routes from './Routes';

import 'crypto-browserify';
import 'stream-browserify';
import 'buffer';
import 'util';


const App = () => {
  const { settings } = useSettings();
  const theme = createTheme(settings);

  return (
    <StyledEngineProvider injectFirst>
      <ThemeProvider theme={theme}>
          <SnackbarProvider maxSnack={1}>
            <Router>
              <Auth>
                <ScrollReset />
                <GoogleAnalytics />
                <CookiesNotification />
                <SettingsNotification />
                <Routes />
              </Auth>
            </Router>
          </SnackbarProvider>
      </ThemeProvider>
    </StyledEngineProvider>
  );
};

export default App;
