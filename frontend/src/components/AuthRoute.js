import React from 'react';
import { useSelector } from 'react-redux';
import { Navigate } from 'react-router-dom';
import PropTypes from 'prop-types';

function AuthRoute({ component: Component, render, ...rest }) {
  const account = useSelector((state) => state.account);

  if (!account.user) {
    return <Navigate to="/login" />;
  }

  return render ? render({ ...rest }) : <Component {...rest} />;
}

AuthRoute.propTypes = {
  component: PropTypes.any,
  render: PropTypes.func
};

export default AuthRoute;
