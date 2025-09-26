// pages/ClinicalTrials/ClinicalTrials.jsx - Updated with collapsible arrows and hook fix
import React, { useState, useEffect, useCallback } from 'react';
import { useAppContext } from '../../context';
import apiService from '../../services/api';
import './ClinicalTrials.css';

const ClinicalTrials = () => {
  const { state } = useAppContext();
  const { user } = state;
  const [trials, setTrials] = useState([]);
  const [filteredTrials, setFilteredTrials] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [expandedTrials, setExpandedTrials] = useState({}); // New state for collapsible
  const [filters, setFilters] = useState({
    category: 'all',
    status: 'all',
    phase: 'all'
  });

  const loadTrials = async () => {
    try {
      setLoading(true);
      const response = await apiService.getClinicalTrials();
      
      if (response.success) {
        setTrials(response.trials || []);
      } else {
        console.error('Failed to load clinical trials');
        setTrials([]);
      }
    } catch (error) {
      console.error('Error loading clinical trials:', error);
      setTrials([]);
    } finally {
      setLoading(false);
    }
  };

  // ✅ FIX: Use useCallback to memoize applyFilters function
  const applyFilters = useCallback(() => {
    let filtered = trials;

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(trial =>
        trial.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        trial.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        trial.vendor.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Category filter
    if (filters.category !== 'all') {
      filtered = filtered.filter(trial => trial.category === filters.category);
    }

    // Status filter
    if (filters.status !== 'all') {
      filtered = filtered.filter(trial => trial.status === filters.status);
    }

    // Phase filter
    if (filters.phase !== 'all') {
      filtered = filtered.filter(trial => trial.clinical_status === filters.phase);
    }

    setFilteredTrials(filtered);
  }, [trials, searchTerm, filters]); // ✅ Include all dependencies

  useEffect(() => {
    loadTrials();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [applyFilters]); // ✅ Now include applyFilters in dependencies

  const handleFilterChange = (filterType, value) => {
    setFilters(prev => ({
      ...prev,
      [filterType]: value
    }));
  };

  // New: Toggle function for collapsible trials
  const handleToggle = (trialId) => {
    setExpandedTrials(prev => ({
      ...prev,
      [trialId]: !prev[trialId]
    }));
  };

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'open': return '#28a745';
      case 'closed': return '#6c757d';
      case 'pending': return '#ffc107';
      default: return '#17a2b8';
    }
  };

  const getStatusLabel = (status) => {
    switch (status?.toLowerCase()) {
      case 'open': return 'Recruiting';
      case 'closed': return 'Completed';
      case 'pending': return 'Not Yet Recruiting';
      default: return 'Active';
    }
  };

  const getPhaseColor = (phase) => {
    switch (phase?.toLowerCase()) {
      case 'ongoing': return '#17a2b8';
      case 'proven': return '#28a745';
      case 'none': return '#6c757d';
      default: return '#f8f9fa';
    }
  };

  const getPhaseLabel = (phase) => {
    switch (phase?.toLowerCase()) {
      case 'ongoing': return 'Phase II';
      case 'proven': return 'Phase III';
      case 'none': return 'Phase I';
      default: return 'Phase';
    }
  };

  const handleLearnMore = (trial) => {
    const confirmed = window.confirm(
      `You are being redirected to ClinicalTrials.gov. Continue?`
    );
    
    if (confirmed) {
      window.open(
        `https://clinicaltrials.gov/search?term=${encodeURIComponent(trial.trial_code || trial.name)}`,
        '_blank'
      );
    }
  };

  const handleContact = (trial) => {
    const confirmed = window.confirm(
      `You are being redirected to contact the study team. Continue?`
    );
    
    if (confirmed) {
      window.open(
        `https://clinicaltrials.gov/search?term=${encodeURIComponent(trial.trial_code || trial.name)}`,
        '_blank'
      );
    }
  };

  if (loading) {
    return (
      <div id="clinical-trials" className="content-section">
        <div className="clinical-trials-container">
          <div className="loading-state">
            <div className="loading-spinner"></div>
            <p>Loading clinical trials...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div id="clinical-trials" className="content-section">
      <div className="clinical-trials-container">
        {/* Header Section */}
        <div className="clinical-trials-header">
          <div className="page-title-container">
            <h1 className="clinical-trials-title">Clinical Trials</h1>
            <div className="last-updated">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
              </svg>
              Last updated: {user.lastUpdated}
            </div>
          </div>
          <p className="clinical-trials-subtitle">
            Discover clinical trials and research studies in microbiome health and wellness. 
            Join cutting-edge research to advance scientific understanding while potentially improving your health.
          </p>
        </div>

        {/* Search and Filters */}
        <div className="search-filter-container">
          <div className="search-bar">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="11" cy="11" r="8"></circle>
              <path d="M21 21l-4.35-4.35"></path>
            </svg>
            <input
              type="text"
              placeholder="Search trials by name, description, or sponsor..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            {searchTerm && (
              <button className="clear-search" onClick={() => setSearchTerm('')}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>
            )}
          </div>

          <div className="filter-controls">
            <select 
              value={filters.category} 
              onChange={(e) => handleFilterChange('category', e.target.value)}
            >
              <option value="all">All Categories</option>
              <option value="gut">Gut Health</option>
              <option value="liver">Liver Health</option>
              <option value="heart">Heart Health</option>
              <option value="cognitive">Cognitive Health</option>
              <option value="aging">Aging & Longevity</option>
              <option value="skin">Skin Health</option>
            </select>

            <select 
              value={filters.status} 
              onChange={(e) => handleFilterChange('status', e.target.value)}
            >
              <option value="all">All Status</option>
              <option value="open">Recruiting</option>
              <option value="closed">Completed</option>
              <option value="pending">Not Yet Recruiting</option>
            </select>

            <select 
              value={filters.phase} 
              onChange={(e) => handleFilterChange('phase', e.target.value)}
            >
              <option value="all">All Phases</option>
              <option value="ongoing">Phase II</option>
              <option value="proven">Phase III</option>
              <option value="none">Phase I</option>
            </select>
          </div>
        </div>

        {/* Results Summary */}
        <div className="results-summary">
          <p>Showing {filteredTrials.length} of {trials.length} clinical trials</p>
        </div>

        {/* Trials List */}
        <div className="trials-grid">
          {filteredTrials.length > 0 ? filteredTrials.map((trial) => {
            const isExpanded = expandedTrials[trial.trial_id] || false;
            
            return (
              <div key={trial.trial_id} className="trial-card">
                {/* Clickable Header */}
                <div 
                  className="trial-header-clickable"
                  onClick={() => handleToggle(trial.trial_id)}
                >
                  <div className="trial-header-content">
                    <div className="trial-title-info">
                      <h3 className="trial-title">{trial.name}</h3>
                      <div className="trial-meta">
                        <span 
                          className="trial-phase"
                          style={{ 
                            backgroundColor: getPhaseColor(trial.clinical_status),
                            color: trial.clinical_status?.toLowerCase() === 'none' ? '#495057' : 'white'
                          }}
                        >
                          {getPhaseLabel(trial.clinical_status)}
                        </span>
                        <span 
                          className="trial-status"
                          style={{ backgroundColor: getStatusColor(trial.status) }}
                        >
                          {getStatusLabel(trial.status)}
                        </span>
                        <span className="trial-duration">{trial.duration}</span>
                      </div>
                    </div>
                    
                    <div className="trial-participation">
                      <div className="participation-info">
                        <span className="participants-count">
                          {trial.participants || 0} / {trial.max_participants || 0}
                        </span>
                        <span className="participants-label">Participants</span>
                      </div>
                      {trial.completion_percentage !== undefined && (
                        <div className="completion-bar">
                          <div 
                            className="completion-fill"
                            style={{ width: `${trial.completion_percentage}%` }}
                          ></div>
                        </div>
                      )}
                    </div>
                    
                    <div className={`trial-arrow ${isExpanded ? 'expanded' : ''}`}>
                      ▼
                    </div>
                  </div>
                </div>

                {/* Expandable Content */}
                {isExpanded && (
                  <div className="trial-expanded-content">
                    <p className="trial-description">{trial.description}</p>
                    
                    {trial.key_findings && (
                      <div className="trial-findings">
                        <strong>Key Findings:</strong> {trial.key_findings}
                      </div>
                    )}
                    
                    <div className="trial-footer">
                      <div className="trial-info">
                        <div className="vendor-info">
                          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                            <circle cx="12" cy="7" r="4"/>
                          </svg>
                          {trial.vendor}
                        </div>
                        {trial.publication && (
                          <div className="publication-info">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
                            </svg>
                            {trial.publication}
                          </div>
                        )}
                      </div>
                      <div className="trial-actions">
                        <button 
                          className="learn-more-btn"
                          onClick={(e) => {
                            e.stopPropagation();
                            handleLearnMore(trial);
                          }}
                        >
                          Learn More
                        </button>
                        <button 
                          className="contact-btn"
                          onClick={(e) => {
                            e.stopPropagation();
                            handleContact(trial);
                          }}
                        >
                          Contact Study Team
                        </button>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            );
          }) : (
            <div className="no-results">
              <p>No clinical trials found matching your criteria.</p>
              <button onClick={() => {
                setSearchTerm('');
                setFilters({ category: 'all', status: 'all', phase: 'all' });
              }}>
                Clear all filters
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ClinicalTrials;