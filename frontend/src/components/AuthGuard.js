import React from 'react';
import { useSelector } from 'react-redux';
import { Navigate } from 'react-router-dom';
import PropTypes from 'prop-types';

function AuthGuard({ children }) {
  const account = useSelector((state) => state.account);

  if (!account.user) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

AuthGuard.propTypes = {
  children: PropTypes.node
};

export default AuthGuard;
