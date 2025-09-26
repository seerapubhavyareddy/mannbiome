// components/Modal/HealthModal.jsx - Enhanced version (Fixed)
import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useAppContext } from '../../context';
import apiService from '../../services/api';
import HealthMetrics from './HealthMetrics';
import SpeciesCarousel from './SpeciesCarousel';
import PathwayCarousel from './PathwayCarousel';
import RecommendationsSection from './RecommendationsSection';
import ClinicalTrialsSection from './ClinicalTrialsSection';
import './HealthModal.css';

const HealthModal = () => {
  const { state, closeModal } = useAppContext();
  const [modalData, setModalData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Check if this is a detailed health domain modal
  const isDetailedDomainModal = state.modal.isOpen && 
    typeof state.modal.content === 'string' && 
    ['liver', 'aging', 'skin', 'cognitive', 'gut', 'heart'].includes(state.modal.content);

  // ✅ FIX: Use useMemo to memoize the domain ID mapping
  const domainIdMap = useMemo(() => ({
    gut: 1,
    liver: 2, 
    heart: 3,
    skin: 4,
    cognitive: 5,
    aging: 6
  }), []); // Empty dependency array since this never changes

  // ✅ FIX: Use useCallback to memoize the function
  const fetchDetailedDomainData = useCallback(async (domainName) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log(`🔍 Fetching detailed data for ${domainName} domain`);
      const domainId = domainIdMap[domainName];
      
      if (!domainId) {
        throw new Error(`Unknown domain: ${domainName}`);
      }

      const response = await apiService.getHealthDomainModalData(domainId, state.customerId);
      
      if (response.success) {
        console.log('✅ Modal data received:', response);
        setModalData(response);
      } else {
        throw new Error(response.message || 'Failed to fetch domain data');
      }
    } catch (err) {
      console.error('❌ Error fetching domain data:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [domainIdMap, state.customerId]); // ✅ Include dependencies

  // ✅ FIX: Now include fetchDetailedDomainData in dependencies
  useEffect(() => {
    if (isDetailedDomainModal) {
      fetchDetailedDomainData(state.modal.content);
    }
  }, [state.modal.content, isDetailedDomainModal, fetchDetailedDomainData]);

  if (!state.modal.isOpen) return null;

  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget) {
      closeModal();
    }
  };

  const renderDetailedDomainContent = () => {
    if (loading) {
      return (
        <div className="modal-loading">
          <div className="loading-spinner"></div>
          <p>Loading {state.modal.content} health details...</p>
        </div>
      );
    }

    if (error) {
      return (
        <div className="modal-error">
          <p>Error loading data: {error}</p>
          <button onClick={() => fetchDetailedDomainData(state.modal.content)}>
            Retry
          </button>
        </div>
      );
    }

    if (!modalData) {
      return <div className="modal-loading">Preparing data...</div>;
    }

    return (
      <div className="detailed-domain-content">
        {/* Back Button */}
        <button className="back-button" onClick={closeModal}>
          ← Back to Overview
        </button>

        {/* Page Title */}
        <h1 className="page-title">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#00BFA5" strokeWidth="2">
            <path d="M12 2a9 9 0 0 1 9 9c0 3.9-2.5 7.2-6 8.4v1.6a1 1 0 0 1-1 1H10a1 1 0 0 1-1-1v-1.6c-3.5-1.2-6-4.5-6-8.4a9 9 0 0 1 9-9z"/>
          </svg>
          {state.modal.content.charAt(0).toUpperCase() + state.modal.content.slice(1)} Health
        </h1>

        {/* Health Metrics */}
        {modalData.health_metrics && (
          <HealthMetrics 
            healthMetrics={modalData.health_metrics}
            domainName={state.modal.content}
          />
        )}

        {/* Species Carousel */}
        {modalData.species_carousel && (
          <SpeciesCarousel speciesData={modalData.species_carousel} />
        )}

        {/* Pathway Carousel */}
        {modalData.pathway_carousel && (
          <PathwayCarousel pathwayData={modalData.pathway_carousel} />
        )}

        {/* Recommendations Section */}
        {modalData.recommendations && (
          <RecommendationsSection recommendations={modalData.recommendations} />
        )}

        {/* Clinical Trials Section */}
        <ClinicalTrialsSection domainId={state.modal.content} />

        {/* Doctor's Remarks Section */}
        <div className="modal-section doctor-remarks-section">
          <h3 className="section-title">
            Remarks from your doctor (if any)
          </h3>
          <div className="doctor-remarks-content">
            {/* Empty space for doctor's remarks - can be made editable later */}
          </div>
        </div>

        {/* Disclaimer Section */}
        <div className="modal-section disclaimer-section">
          <h4 className="disclaimer-title">Disclaimer</h4>
          <p className="disclaimer-text">
            These recommendations are based on your current microbiome analysis and should be discussed 
            with your healthcare provider before making any changes to your regimen. Individual results may vary.
          </p>
        </div>
      </div>
    );
  };

  const renderRegularModalContent = () => {
    return (
      <div 
        className="modal-content-wrapper"
        dangerouslySetInnerHTML={{ __html: state.modal.content }}
      />
    );
  };

  return (
    <div className="modal-backdrop" onClick={handleBackdropClick}>
      <div className="modal-container">
        <div className="modal-header">
          <h2 className="modal-title">{state.modal.title}</h2>
          <button className="modal-close" onClick={closeModal}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div className="modal-content">
          {isDetailedDomainModal ? renderDetailedDomainContent() : renderRegularModalContent()}
        </div>
      </div>
    </div>
  );
};

export default HealthModal;