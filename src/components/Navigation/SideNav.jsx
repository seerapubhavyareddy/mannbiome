// components/Navigation/SideNav.jsx
import React from 'react';
import { useAppContext } from '../../context';
import { useScrollSpy } from '../../hooks/useScrollSpy';
import './SideNav.css';

const SideNav = () => {
  const { state, setActiveSection } = useAppContext();
  const { user, activeSection } = state;

  // Use scroll spy to track active section
  useScrollSpy(['current-report', 'analysis', 'recommendations', 'download']);

  const navItems = [
    {
      id: 'current-report',
      label: 'Current Report',
      icon: (
        <>
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
          <polyline points="14 2 14 8 20 8"></polyline>
          <line x1="16" y1="13" x2="8" y2="13"></line>
          <line x1="16" y1="17" x2="8" y2="17"></line>
          <polyline points="10 9 9 9 8 9"></polyline>
        </>
      )
    },
    {
      id: 'analysis',
      label: 'Analysis',
      icon: <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
    },
    {
      id: 'recommendations',
      label: 'Recommendations',
      icon: (
        <>
          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
          <polyline points="22 4 12 14.01 9 11.01"></polyline>
        </>
      )
    },
    {
      id: 'download',
      label: 'Download',
      icon: (
        <>
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
          <polyline points="7 10 12 15 17 10"></polyline>
          <line x1="12" y1="15" x2="12" y2="3"></line>
        </>
      )
    }
  ];

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
      setActiveSection(sectionId);
    }
  };

  return (
    <div className="side-nav">
      <div className="side-nav-header">
        <h3 className="side-nav-title">Report Navigation</h3>
        <div className="side-nav-subtitle">{user.reportId} | {user.lastUpdated}</div>
      </div>
      
      {navItems.map((item) => (
        <div
          key={item.id}
          className={`side-nav-item ${activeSection === item.id ? 'active' : ''}`}
          onClick={() => scrollToSection(item.id)}
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            {item.icon}
          </svg>
          {item.label}
        </div>
      ))}
    </div>
  );
};

export default SideNav;