import React, {
  lazy,
  Suspense
} from 'react';
import {
  Routes,
  Navigate,
  Route
} from 'react-router-dom';
import DashboardLayout from './layouts/DashboardLayout';
import MainLayout from './layouts/MainLayout';
import HomeView from './views/pages/HomeView';
import LoadingScreen from './components/LoadingScreen';
import AuthRoute from './components/AuthRoute';
import GuestRoute from './components/GuestRoute';

function AppRoutes() {
  return (
    <Suspense fallback={<LoadingScreen />}>
      <Routes>
        <Route
          path="/"
          element={<Navigate replace to="/home" />}
        />
        <Route
          exact
          path="/404"
          component={lazy(() => import('./views/pages/Error404View'))}
        />
        <GuestRoute
          exact
          path="/login"
          component={lazy(() => import('./views/auth/LoginView'))}
        />
        <Route
          exact
          path="/login-unprotected"
          component={lazy(() => import('./views/auth/LoginView'))}
        />
        <GuestRoute
          exact
          path="/register"
          component={lazy(() => import('./views/auth/RegisterView'))}
        />
        <Route
          exact
          path="/register-unprotected"
          component={lazy(() => import('./views/auth/RegisterView'))}
        />
        <AuthRoute
          path="/app"
          render={(props) => (
            <DashboardLayout {...props}>
              <Suspense fallback={<LoadingScreen />}>
                <Routes>
                  <Navigate
                    exact
                    from="/app"
                    to="/app/reports/dashboard"
                  />
                  <Route
                    exact
                    path="/app/account"
                    component={lazy(() => import('./views/pages/AccountView'))}
                  />
                  <Route
                    exact
                    path="/app/reports/dashboard"
                    component={lazy(() => import('./views/reports/DashboardView'))}
                  />
                  <Route
                    exact
                    path="/app/reports/dashboard-alternative"
                    component={lazy(() => import('./views/reports/DashboardAlternativeView'))}
                  />
                  <Navigate
                    exact
                    from="app/reports"
                    to="/app/reports/dashboard"
                  />
                  <Route
                    exact
                    path="/app/management/customers"
                    component={lazy(() => import('./views/management/CustomerListView'))}
                  />
                  <Route
                    exact
                    path="/app/management/customers/:id"
                    component={lazy(() => import('./views/management/CustomerDetailsView'))}
                  />
                  <Route
                    exact
                    path="/app/management/customers/:id/edit"
                    component={lazy(() => import('./views/management/CustomerEditView'))}
                  />
                  <Route
                    exact
                    path="/app/projects/overview"
                    component={lazy(() => import('./views/projects/OverviewView'))}
                  />
                  <Route
                    exact
                    path="/app/projects/browse"
                    component={lazy(() => import('./views/projects/ProjectBrowseView'))}
                  />
                  <Route
                    exact
                    path="/app/projects/create"
                    component={lazy(() => import('./views/projects/ProjectCreateView'))}
                  />
                  <Route
                    exact
                    path="/app/projects/:id"
                    component={lazy(() => import('./views/projects/ProjectDetailsView'))}
                  />
                  <Route
                    exact
                    path="/app/extra/charts/apex"
                    component={lazy(() => import('./views/extra/charts/ApexChartsView'))}
                  />
                  <Navigate to="/404" />
                </Routes>
              </Suspense>
            </DashboardLayout>
          )}
        />
        <Route
          path="*"
          render={(props) => (
            <MainLayout {...props}>
              <Routes>
                <Route
                  exact
                  path="/home"
                  component={HomeView}
                />
                <Navigate to="/404" />
              </Routes>
            </MainLayout>
          )}
        />
        <Navigate to="/404" />
      </Routes>
    </Suspense>
  );
}

export default AppRoutes;
