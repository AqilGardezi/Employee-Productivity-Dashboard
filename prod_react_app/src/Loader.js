import React from 'react';
import './Spinner.css';

const ModernLoader = ({ isLoading }) => {
  return isLoading ? (
    <div className="modern-loader"></div>
  ) : null;
};

export default ModernLoader;