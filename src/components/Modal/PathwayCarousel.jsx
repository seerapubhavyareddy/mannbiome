// components/Modal/PathwayCarousel.jsx
import React, { useState } from 'react';
import './PathwayCarousel.css';

const PathwayCarousel = ({ pathwayData }) => {
  const [currentSlide, setCurrentSlide] = useState(0);

  // Process pathway data from API structure
  const processPathwayData = () => {
    if (!pathwayData || typeof pathwayData !== 'object') {
      return [];
    }

    // Convert object to array for carousel
    return Object.entries(pathwayData).map(([key, data]) => ({
      category: data.title || key,
      status: data.status || 'Unknown',
      metrics: data.metrics || []
    }));
  };

  const processedData = processPathwayData();

  if (processedData.length === 0) {
    return (
      <div className="pathway-carousel-loading">
        <p>Loading pathway data...</p>
      </div>
    );
  }

  const moveToSlide = (slideIndex) => {
    setCurrentSlide(slideIndex);
  };

  const PathwayItem = ({ metric }) => (
    <div className="pathway-item">
      <h4>{metric.name}</h4>
      <div className="range-bar">
        <div 
          className="range-fill" 
          style={{ width: `${metric.range_fill_width || 0}%` }}
        ></div>
        <div 
          className="range-marker" 
          style={{ left: `${metric.marker_position || 0}%` }}
        ></div>
      </div>
      <div className="range-values">
        <span>{metric.range_low || 'Low'}</span>
        <span>{metric.range_high || 'High'}</span>
      </div>
    </div>
  );

  const PathwayCard = ({ category, data }) => (
    <div className="pathway-card">
      <div className="pathway-title">
        <span>{category}</span>
        <span>Status: {data.status || 'Normal'}</span>
      </div>
      <div className="pathway-grid">
        {data.metrics && data.metrics.length > 0 ? (
          data.metrics.map((metric, index) => (
            <PathwayItem key={index} metric={metric} />
          ))
        ) : (
          <div className="no-pathway-data">No pathway data available</div>
        )}
      </div>
    </div>
  );

  return (
    <div className="pathway-section">
      <h2 className="section-title">Metabolic Pathways</h2>
      
      <div className="carousel">
        <div className="carousel-track">
          <div 
            className="carousel-slides-container"
            style={{ transform: `translateX(-${currentSlide * 100}%)` }}
          >
            {processedData.map((categoryData, index) => (
              <div key={index} className="carousel-slide">
                <PathwayCard 
                  category={categoryData.category} 
                  data={categoryData} 
                />
              </div>
            ))}
          </div>
        </div>

        {/* Navigation Dots */}
        <div className="carousel-dots">
          {processedData.map((_, index) => (
            <span
              key={index}
              className={`dot ${index === currentSlide ? 'active' : ''}`}
              onClick={() => moveToSlide(index)}
            ></span>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PathwayCarousel;