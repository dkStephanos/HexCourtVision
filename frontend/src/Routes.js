import React, { lazy, Suspense } from 'react';
import { useSelector } from 'react-redux';
import { Routes, Route, Navigate } from 'react-router-dom';
import DashboardLayout from './layouts/DashboardLayout';
import MainLayout from './layouts/MainLayout';
import HomeView from './views/pages/HomeView';
import LoadingScreen from './components/LoadingScreen';

// Lazy loaded views
const Error404View = lazy(() => import('./views/pages/Error404View'));
const LoginView = lazy(() => import('./views/auth/LoginView'));
const RegisterView = lazy(() => import('./views/auth/RegisterView'));
const AccountView = lazy(() => import('./views/pages/AccountView'));
const DashboardView = lazy(() => import('./views/reports/DashboardView'));
const DashboardAlternativeView = lazy(() => import('./views/reports/DashboardAlternativeView'));
const CustomerListView = lazy(() => import('./views/management/CustomerListView'));
const CustomerDetailsView = lazy(() => import('./views/management/CustomerDetailsView'));
const CustomerEditView = lazy(() => import('./views/management/CustomerEditView'));
const OverviewView = lazy(() => import('./views/projects/OverviewView'));
const ProjectBrowseView = lazy(() => import('./views/projects/ProjectBrowseView'));
const ProjectCreateView = lazy(() => import('./views/projects/ProjectCreateView'));
const ProjectDetailsView = lazy(() => import('./views/projects/ProjectDetailsView'));
const ApexChartsView = lazy(() => import('./views/extra/charts/ApexChartsView'));

function AppRoutes() {
  const account = useSelector((state) => state.account);

  return (
    <Suspense fallback={<LoadingScreen />}>
      <Routes>
        <Route path="/" element={<Navigate replace to="/home" />} />
        <Route path="/404" element={<Error404View />} />
        <Route path="/login" element={account.user ? <Navigate replace to="/" /> : <LoginView />} />
        <Route path="/login-unprotected" element={<LoginView />} />
        <Route path="/register" element={account.user ? <Navigate replace to="/" /> : <RegisterView />} />
        <Route path="/register-unprotected" element={<RegisterView />} />
        <Route path="/app/*" element={<DashboardLayout />}>
          {/* Nested routes for DashboardLayout */}
          <Route index element={<Navigate replace to="reports/dashboard" />} />
          <Route path="account" element={<AccountView />} />
          <Route path="reports/dashboard" element={<DashboardView />} />
          <Route path="reports/dashboard-alternative" element={<DashboardAlternativeView />} />
          <Route path="management/customers" element={<CustomerListView />} />
          <Route path="management/customers/:id" element={<CustomerDetailsView />} />
          <Route path="management/customers/:id/edit" element={<CustomerEditView />} />
          <Route path="projects/overview" element={<OverviewView />} />
          <Route path="projects/browse" element={<ProjectBrowseView />} />
          <Route path="projects/create" element={<ProjectCreateView />} />
          <Route path="projects/:id" element={<ProjectDetailsView />} />
          <Route path="extra/charts/apex" element={<ApexChartsView />} />
          <Route path="*" element={<Navigate to="/404" />} />
        </Route>
        <Route path="*" element={<MainLayout />}>
          {/* Nested routes for MainLayout */}
          <Route path="home" element={<HomeView />} />
          <Route path="*" element={<Navigate to="/404" />} />
        </Route>
      </Routes>
    </Suspense>
  );
}

export default AppRoutes;
