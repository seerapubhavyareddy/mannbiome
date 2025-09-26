// components/Modal/HealthMetrics.jsx
import React from 'react';
import './HealthMetrics.css';

const HealthMetrics = ({ healthMetrics, domainName }) => {
  if (!healthMetrics || !Array.isArray(healthMetrics)) {
    return (
      <div className="health-metrics-loading">
        <p>Loading health metrics...</p>
      </div>
    );
  }

  return (
    <div className="health-metrics-container">
      <div className="health-metrics-grid">
        {healthMetrics.map((metric, index) => (
          <div key={index} className="health-metric-card">
            <div className="metric-label">
              {metric.label}
            </div>
            <div className="metric-value">
              {typeof metric.value === 'number' ? metric.value.toFixed(1) : metric.value}
            </div>
            <div className="metric-description">
              {metric.description}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default HealthMetrics;