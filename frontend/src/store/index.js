import { configureStore as configureToolkitStore } from '@reduxjs/toolkit';
import { thunk } from 'redux-thunk';
import { createLogger } from 'redux-logger';
import rootReducer from '../reducers';
import { ENABLE_REDUX_LOGGER } from '../config';

const loggerMiddleware = createLogger();

export function configureStore(preloadedState = {}) {
  const middlewares = [thunk];

  if (ENABLE_REDUX_LOGGER) {
    middlewares.push(loggerMiddleware);
  }

  const store = configureToolkitStore({
    reducer: rootReducer,
    middleware: (getDefaultMiddleware) => 
      getDefaultMiddleware().concat(middlewares),
    preloadedState,
    devTools: process.env.NODE_ENV !== 'production', // Optional: DevTools setup
  });

  return store;
}

