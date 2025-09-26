// components/Test/TestModalComponents.jsx
// This is a temporary component to test the new modal components

import React, { useState } from 'react';
import HealthMetrics from '../Modal/HealthMetrics';
import SpeciesCarousel from '../Modal/SpeciesCarousel';

const TestModalComponents = () => {
  const [activeTest, setActiveTest] = useState('health-metrics');

  // Mock data for testing
  const mockHealthMetrics = [
    {
      label: "Status Level",
      value: "Excellent",
      unit: "level",
      description: "Your Gut markers show strong health indicators"
    },
    {
      label: "Score",
      value: 3.8,
      unit: "score", 
      description: "Above average Gut health score"
    },
    {
      label: "Diversity",
      value: 3.2,
      unit: "index",
      description: "High microbial diversity observed"
    }
  ];

  const mockSpeciesData = [
    {
      category: "Top Bacterial Species",
      status: "Excellent",
      species: [
        {
          name: "Bacteroides fragilis",
          range_fill_width: 75,
          marker_position: 80,
          range_low: "10⁴ CFU/g",
          range_high: "10⁸ CFU/g"
        },
        {
          name: "Escherichia coli",
          range_fill_width: 65,
          marker_position: 70,
          range_low: "10³ CFU/g",
          range_high: "10⁷ CFU/g"
        },
        {
          name: "Lactobacillus plantarum",
          range_fill_width: 80,
          marker_position: 85,
          range_low: "10⁵ CFU/g",
          range_high: "10⁹ CFU/g"
        },
        {
          name: "Bifidobacterium bifidum",
          range_fill_width: 70,
          marker_position: 75,
          range_low: "10⁴ CFU/g",
          range_high: "10⁸ CFU/g"
        }
      ]
    },
    {
      category: "Probiotic Organisms",
      status: "Excellent",
      species: [
        {
          name: "Lactobacillus acidophilus",
          range_fill_width: 85,
          marker_position: 90,
          range_low: "10⁶ CFU/g",
          range_high: "10⁸ CFU/g"
        },
        {
          name: "Bifidobacterium longum",
          range_fill_width: 75,
          marker_position: 80,
          range_low: "10⁵ CFU/g",
          range_high: "10⁷ CFU/g"
        },
        {
          name: "Lactobacillus rhamnosus",
          range_fill_width: 80,
          marker_position: 85,
          range_low: "10⁶ CFU/g",
          range_high: "10⁸ CFU/g"
        },
        {
          name: "Lactobacillus casei",
          range_fill_width: 90,
          marker_position: 95,
          range_low: "10⁶ CFU/g",
          range_high: "10⁸ CFU/g"
        }
      ]
    },
    {
      category: "Pathogenic Species",
      status: "Low (Good)",
      species: [
        {
          name: "Clostridium difficile",
          range_fill_width: 20,
          marker_position: 25,
          range_low: "10¹ CFU/g",
          range_high: "10³ CFU/g"
        },
        {
          name: "Salmonella enterica",
          range_fill_width: 15,
          marker_position: 20,
          range_low: "10¹ CFU/g",
          range_high: "10³ CFU/g"
        }
      ]
    }
  ];

  return (
    <div style={{ 
      padding: '20px', 
      background: '#f5f5f5', 
      minHeight: '100vh',
      fontFamily: 'Arial, sans-serif'
    }}>
      <h1 style={{ color: '#2C3E50', marginBottom: '20px' }}>
        Test Modal Components
      </h1>
      
      {/* Test Navigation */}
      <div style={{ 
        marginBottom: '30px',
        display: 'flex',
        gap: '10px',
        flexWrap: 'wrap'
      }}>
        <button
          onClick={() => setActiveTest('health-metrics')}
          style={{
            padding: '10px 20px',
            background: activeTest === 'health-metrics' ? '#00BFA5' : '#fff',
            color: activeTest === 'health-metrics' ? '#fff' : '#333',
            border: '1px solid #00BFA5',
            borderRadius: '8px',
            cursor: 'pointer'
          }}
        >
          Health Metrics
        </button>
        <button
          onClick={() => setActiveTest('species-carousel')}
          style={{
            padding: '10px 20px',
            background: activeTest === 'species-carousel' ? '#00BFA5' : '#fff',
            color: activeTest === 'species-carousel' ? '#fff' : '#333',
            border: '1px solid #00BFA5',
            borderRadius: '8px',
            cursor: 'pointer'
          }}
        >
          Species Carousel
        </button>
      </div>

      {/* Test Content */}
      {activeTest === 'health-metrics' && (
        <div>
          <h2 style={{ color: '#2C3E50', marginBottom: '20px' }}>
            Health Metrics Component Test
          </h2>
          <HealthMetrics 
            healthMetrics={mockHealthMetrics}
            domainName="gut"
          />
        </div>
      )}

      {activeTest === 'species-carousel' && (
        <div>
          <h2 style={{ color: '#2C3E50', marginBottom: '20px' }}>
            Species Carousel Component Test
          </h2>
          <SpeciesCarousel speciesData={mockSpeciesData} />
        </div>
      )}

      {/* API Test Button */}
      <div style={{ 
        marginTop: '40px',
        padding: '20px',
        background: '#fff',
        borderRadius: '8px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
      }}>
        <h3 style={{ color: '#2C3E50', marginBottom: '15px' }}>
          API Integration Test
        </h3>
        <p style={{ color: '#666', marginBottom: '15px' }}>
          Click a domain card in your dashboard to test the modal with real API data.
          The enhanced HealthModal should now display the Health Metrics and Species Carousel components.
        </p>
        <p style={{ color: '#666', fontSize: '14px' }}>
          <strong>Next steps:</strong> After testing these components, we'll implement:
          <br />• PathwayCarousel component
          <br />• RecommendationsSection component
          <br />• Enhanced styling and interactions
        </p>
      </div>
    </div>
  );
};

export default TestModalComponents;