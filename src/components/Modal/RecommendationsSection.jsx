// components/Modal/RecommendationsSection.jsx
import React from 'react';
import './RecommendationsSection.css';

const RecommendationsSection = ({ recommendations }) => {
  if (!recommendations || typeof recommendations !== 'object') {
    return (
      <div className="recommendations-loading">
        <p>Loading recommendations...</p>
      </div>
    );
  }

  // Helper function to render recommendation items
  const renderRecommendationItems = (items, categoryName) => {
    if (!items || !Array.isArray(items) || items.length === 0) {
      return (
        <div className="no-recommendations">
          No {categoryName.toLowerCase()} recommendations available
        </div>
      );
    }

    return (
      <ul className="recommendation-list">
        {items
          .filter(item => item.recommended)
          .map((item, index) => (
            <li key={index} className="recommendation-item">
              <div className="recommendation-content">
                <span className="recommendation-name">{item.name}</span>
                <span className="recommendation-checkmark">✓</span>
              </div>
              {item.description && (
                <div className="recommendation-description">{item.description}</div>
              )}
              {item.dosage && (
                <div className="recommendation-dosage">
                  <strong>Dosage:</strong> {item.dosage}
                </div>
              )}
              {item.reason && (
                <div className="recommendation-reason">
                  <strong>Why:</strong> {item.reason}
                </div>
              )}
            </li>
          ))}
      </ul>
    );
  };

  return (
    <div className="recommendations-section">
      <h2 className="section-title">Recommendations</h2>
      
      <div className="recommendations-grid">
        {/* Probiotics Card */}
        {recommendations.probiotics && (
          <div className="recommendation-card">
            <div className="recommendation-card-header">
              <h3 className="recommendation-card-title">Probiotics</h3>
            </div>
            {renderRecommendationItems(recommendations.probiotics, 'Probiotics')}
          </div>
        )}

        {/* Supplements Card */}
        {recommendations.supplements && (
          <div className="recommendation-card">
            <div className="recommendation-card-header">
              <h3 className="recommendation-card-title">Supplements</h3>
            </div>
            {renderRecommendationItems(recommendations.supplements, 'Supplements')}
          </div>
        )}

        {/* Diet Card */}
        {recommendations.diet && (
          <div className="recommendation-card">
            <div className="recommendation-card-header">
              <h3 className="recommendation-card-title">Diet & Nutrition</h3>
            </div>
            {renderRecommendationItems(recommendations.diet, 'Diet')}
          </div>
        )}

        {/* Lifestyle Card */}
        {recommendations.lifestyle && (
          <div className="recommendation-card">
            <div className="recommendation-card-header">
              <h3 className="recommendation-card-title">Lifestyle</h3>
            </div>
            {renderRecommendationItems(recommendations.lifestyle, 'Lifestyle')}
          </div>
        )}
      </div>
    </div>
  );
};

export default RecommendationsSection;