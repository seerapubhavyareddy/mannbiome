// hooks/useModal.js
import { useState, useCallback } from 'react';

export const useModal = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [content, setContent] = useState(null);

  const loadContent = useCallback(async (source) => {
    setIsLoading(true);
    setError(null);
    
    try {
      // In a real application, you would fetch the content from a file or API
      // For now, we'll simulate loading content
      await new Promise(resolve => setTimeout(resolve, 500)); // Simulate loading
      
      // Mock content - in reality, you'd fetch from the source file
      const mockContent = `
        <div style="padding: 20px; font-family: Arial, sans-serif;">
          <h3 style="color: #2C3E50; margin-bottom: 15px;">Detailed Health Information</h3>
          <p style="color: #555; line-height: 1.6; margin-bottom: 15px;">
            This would contain the content loaded from ${source}. In a real implementation, 
            you would fetch this content from your server or load it from static files.
          </p>
          <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
            <h4 style="color: #343a40; margin-bottom: 10px;">Key Metrics</h4>
            <ul style="color: #555; padding-left: 20px;">
              <li>Health Score: Based on microbiome analysis</li>
              <li>Diversity Index: Measures species variety</li>
              <li>Risk Factors: Identified areas of concern</li>
              <li>Recommendations: Personalized suggestions</li>
            </ul>
          </div>
          <p style="color: #555; line-height: 1.6;">
            For the complete analysis and detailed recommendations, please refer to your 
            full report or consult with your healthcare provider.
          </p>
        </div>
      `;
      
      setContent(mockContent);
    } catch (err) {
      setError(err.message || 'Failed to load content');
    } finally {
      setIsLoading(false);
    }
  }, []);

  return {
    isLoading,
    error,
    content,
    loadContent
  };
};