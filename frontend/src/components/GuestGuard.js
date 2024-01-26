import React from 'react';
import { useSelector } from 'react-redux';
import { Navigate } from 'react-router-dom';
import PropTypes from 'prop-types';

function GuestGuard({ children }) {
  const account = useSelector((state) => state.account);

  if (account.user) {
    return <Navigate to="/app/account" replace />;
  }

  return children;
}

GuestGuard.propTypes = {
  children: PropTypes.node
};

export default GuestGuard;
