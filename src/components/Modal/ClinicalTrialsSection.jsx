// components/Modal/ClinicalTrialsSection.jsx
import React, { useState, useEffect } from 'react';
import { useAppContext } from '../../context';
import apiService from '../../services/api';
import './ClinicalTrialsSection.css';

const ClinicalTrialsSection = ({ domainId }) => {
  const { state } = useAppContext();
  const [trials, setTrials] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expandedTrials, setExpandedTrials] = useState({});

  // Fetch clinical trials for this domain
  useEffect(() => {
    const fetchTrials = async () => {
      try {
        setLoading(true);
        const response = await apiService.getDomainClinicalTrials(domainId, state.customerId);
        
        if (response.success && response.trials) {
          // Filter only eligible trials
          const eligibleTrials = response.trials.filter(trial => trial.is_eligible);
          setTrials(eligibleTrials);
        }
      } catch (error) {
        console.error('Error fetching clinical trials:', error);
        setTrials([]);
      } finally {
        setLoading(false);
      }
    };

    if (domainId && state.customerId) {
      fetchTrials();
    }
  }, [domainId, state.customerId]);

  // Simple toggle function using object instead of Set
  const handleToggle = (trialId) => {
    console.log('🔄 Toggling trial ID:', trialId);
    setExpandedTrials(prev => {
      const newState = {
        ...prev,
        [trialId]: !prev[trialId]
      };
      console.log('📋 New expanded state:', newState);
      return newState;
    });
  };

  // Handle external link with confirmation
  const handleExternalLink = (url, siteName) => {
    const confirmed = window.confirm(
      `You are being redirected to ${siteName || 'an external website'}. Continue?`
    );
    
    if (confirmed) {
      window.open(url, '_blank', 'noopener,noreferrer');
    }
  };

  // Don't render if loading, no trials, or no eligible trials
  if (loading || trials.length === 0) {
    return null;
  }

  return (
    <div className="clinical-trials-section">
      <h2 className="section-title">Clinical Trials</h2>
      <p className="section-description">
        Relevant clinical trials for your {domainId} health based on your profile
      </p>
      
      <div className="trials-list">
        {trials.map((trial) => {
          const isExpanded = expandedTrials[trial.trial_id] || false;
          const completionPercentage = trial.max_participants > 0 
            ? Math.round((trial.participants / trial.max_participants) * 100)
            : 0;

          return (
            <div key={trial.trial_id} className="trial-card">
              {/* Header - Clickable Row */}
              <div 
                className="trial-header"
                onClick={() => handleToggle(trial.trial_id)}
              >
                <div className="trial-header-content">
                  {/* Trial Name */}
                  <div className="trial-name">
                    {trial.name}
                  </div>
                  
                  {/* Status and Participants */}
                  <div className="trial-meta">
                    <span className={`trial-status status-${trial.status?.toLowerCase() || 'unknown'}`}>
                      {trial.status?.toUpperCase() || 'UNKNOWN'}
                    </span>
                    <span className="trial-participants">
                      {trial.participants || 0}/{trial.max_participants || 0} participants
                    </span>
                    {completionPercentage > 0 && (
                      <span className="completion-percentage">
                        ({completionPercentage}% full)
                      </span>
                    )}
                  </div>
                  
                  {/* Arrow */}
                  <div className={`trial-arrow ${isExpanded ? 'expanded' : ''}`}>
                    ▼
                  </div>
                </div>
              </div>

              {/* Expanded Content */}
              {isExpanded && (
                <div className="trial-details">
                  <div className="trial-description">
                    <p>{trial.description}</p>
                  </div>
                  
                  <div className="trial-info-grid">
                    <div className="trial-info-item">
                      <strong>Duration:</strong> {trial.duration || 'Not specified'}
                    </div>
                    <div className="trial-info-item">
                      <strong>Clinical Status:</strong> {trial.clinical_status || 'Not specified'}
                    </div>
                    {trial.vendor && (
                      <div className="trial-info-item">
                        <strong>Sponsor:</strong> {trial.vendor}
                      </div>
                    )}
                    {trial.eligibility_reason && (
                      <div className="trial-info-item eligibility-info">
                        <strong>Eligibility:</strong> {trial.eligibility_reason}
                      </div>
                    )}
                  </div>

                  {trial.key_findings && (
                    <div className="trial-findings">
                      <strong>Key Findings:</strong>
                      <p>{trial.key_findings}</p>
                    </div>
                  )}

                  <div className="trial-actions">
                    <button 
                      className="enroll-button"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleExternalLink(
                          `https://clinicaltrials.gov/search?term=${encodeURIComponent(trial.trial_code || trial.name)}`,
                          'ClinicalTrials.gov'
                        );
                      }}
                    >
                      Learn More
                    </button>
                    
                    {trial.status === 'open' && (
                      <button 
                        className="enroll-button primary"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleExternalLink(
                            `https://clinicaltrials.gov/search?term=${encodeURIComponent(trial.trial_code || trial.name)}`,
                            'ClinicalTrials.gov'
                          );
                        }}
                      >
                        Enroll Now
                      </button>
                    )}
                  </div>

                  {trial.publication && trial.publication_date && (
                    <div className="trial-publication">
                      <small>
                        Published in {trial.publication} on {new Date(trial.publication_date).toLocaleDateString()}
                      </small>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
      
      <div className="trials-disclaimer">
        <p>
          <strong>Note:</strong> Participation in clinical trials is voluntary. 
          Please consult with your healthcare provider before enrolling in any study.
        </p>
      </div>
    </div>
  );
};

export default ClinicalTrialsSection;