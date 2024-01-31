import React from 'react';
import { useSelector } from 'react-redux';
import { Navigate } from 'react-router-dom';
import PropTypes from 'prop-types';

function GuestRoute({ component: Component, render, ...rest }) {
  const account = useSelector((state) => state.account);

  if (account.user) {
    return <Navigate to="/" />;
  }

  return render ? render({ ...rest }) : <Component {...rest} />;
}

GuestRoute.propTypes = {
  component: PropTypes.any,
  render: PropTypes.func
};

export default GuestRoute;
