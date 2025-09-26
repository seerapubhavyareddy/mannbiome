// hooks/useScrollSpy.js
import { useEffect } from 'react';
import { useAppContext } from '../context';

export const useScrollSpy = (sectionIds) => {
  const { setActiveSection } = useAppContext();

  useEffect(() => {
    const observers = [];
    
    const observerOptions = {
      root: null,
      rootMargin: '-100px 0px -50% 0px',
      threshold: 0
    };

    const observerCallback = (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          setActiveSection(entry.target.id);
        }
      });
    };

    const observer = new IntersectionObserver(observerCallback, observerOptions);

    sectionIds.forEach(id => {
      const element = document.getElementById(id);
      if (element) {
        observer.observe(element);
        observers.push({ observer, element });
      }
    });

    // Cleanup
    return () => {
      observers.forEach(({ observer: obs, element }) => {
        obs.unobserve(element);
      });
    };
  }, [sectionIds, setActiveSection]);
};