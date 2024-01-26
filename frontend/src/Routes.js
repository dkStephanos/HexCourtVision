/* eslint-disable react/no-array-index-key */
import React, { lazy, Suspense, Fragment } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import DashboardLayout from './layouts/DashboardLayout';
import MainLayout from './layouts/MainLayout';
import HomeView from './views/pages/HomeView';
import LoadingScreen from './components/LoadingScreen';
import AuthGuard from './components/AuthGuard';
import GuestGuard from './components/GuestGuard';

const routesConfig = [
  {
    exact: true,
    path: '/',
    component: () => <Navigate to="/home" replace />
  },
  // ... other routes
  {
    path: '/app',
    guard: AuthGuard,
    layout: DashboardLayout,
    routes: [
      {
        exact: true,
        path: '/app',
        component: () => <Navigate to="/app/reports/dashboard" replace />
      },
      // ... other nested routes
      {
        exact: true,
        path: '/app/management',
        component: () => <Navigate to="/app/management/customers" replace />
      },
      // ... more nested routes
      {
        component: () => <Navigate to="/404" replace />
      }
    ]
  },
  {
    path: '*',
    layout: MainLayout,
    routes: [
      {
        exact: true,
        path: '/home',
        component: HomeView
      },
      {
        component: () => <Navigate to="/404" replace />
      }
    ]
  }
];

const renderRoutes = (routes) => (routes ? (
  <Suspense fallback={<LoadingScreen />}>
    <Routes>
      {routes.map((route, i) => {
        const Guard = route.guard || Fragment;
        const Layout = route.layout || Fragment;
        const Component = route.component;

        return (
          <Route
            key={i}
            path={route.path}
            element={
              <Guard>
                <Layout>
                  {route.routes
                    ? renderRoutes(route.routes)
                    : <Component />}
                </Layout>
              </Guard>
            }
          />
        );
      })}
    </Routes>
  </Suspense>
) : null);

function RoutesWrapper() {
  return renderRoutes(routesConfig);
}

export default RoutesWrapper;
