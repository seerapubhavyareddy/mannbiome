// hooks/useDownload.js
import { useState } from 'react';

export const useDownload = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const downloadReport = async (reportType, domains, customerId) => {
    setIsLoading(true);
    setError(null);

    try {
      // Validate required parameters
      if (!customerId) {
        throw new Error('Customer ID is required for report generation');
      }

      console.log(`Starting download for customer ${customerId}, type: ${reportType}, domains:`, domains);

      // Use the customer-specific endpoint
      const url = `https://gnss5bq5km.us-east-2.awsapprunner.com/api/customer/${customerId}/reports/generate`;
      const requestBody = {
        type: reportType,
        domains: domains || [],
        format: 'pdf',
        customer_id: customerId
      };

      console.log('Making request to:', url);
      console.log('Request body:', requestBody);

      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/pdf, application/json',
          // Add authentication headers if needed
          // 'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(requestBody)
      });

      console.log('Response status:', response.status);
      console.log('Response headers:', Object.fromEntries(response.headers.entries()));

      if (!response.ok) {
        // Try to get error details from response
        let errorMessage = `Failed to generate report (Error ${response.status})`;
        
        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorData.message || errorMessage;
        } catch (jsonError) {
          console.warn('Could not parse error response as JSON');
        }

        // Handle specific error codes
        if (response.status === 404) {
          throw new Error('Customer data not found. Please contact support.');
        } else if (response.status === 400) {
          throw new Error(`Invalid request: ${errorMessage}`);
        } else if (response.status === 503) {
          throw new Error('Service temporarily unavailable. Please try again later.');
        } else if (response.status >= 500) {
          throw new Error('Server error occurred. Please try again or contact support.');
        } else {
          throw new Error(errorMessage);
        }
      }

      // Check the content type to ensure we're getting the expected format
      const contentType = response.headers.get('content-type');
      console.log('Response content type:', contentType);

      // Validate that we received a PDF or at least binary content
      if (contentType && !contentType.includes('pdf') && !contentType.includes('octet-stream')) {
        console.warn('Unexpected content type:', contentType);
        // Don't throw error, but log warning
      }

      // Get the blob with the correct MIME type
      const blob = await response.blob();
      console.log('Received blob size:', blob.size, 'bytes');
      
      // Validate blob size
      if (blob.size === 0) {
        throw new Error('Received empty report file');
      }

      // Validate minimum reasonable PDF size (PDF header is usually ~100+ bytes)
      if (blob.size < 100) {
        throw new Error('Received file appears to be corrupted or incomplete');
      }

      // Ensure the blob has the correct type
      const correctedBlob = new Blob([blob], { 
        type: contentType || 'application/pdf'
      });

      // Generate filename with proper extension and customer info
      const timestamp = new Date().toISOString().slice(0, 10);
      const timeString = new Date().toISOString().slice(11, 19).replace(/:/g, '-');
      
      const reportName = reportType === 'full' 
        ? `mannbiome-full-report-${customerId}-${timestamp}-${timeString}` 
        : `mannbiome-domain-report-${domains.join('-')}-${customerId}-${timestamp}-${timeString}`;
      
      // Determine file extension based on content type
      let extension = '.pdf';
      if (contentType) {
        if (contentType.includes('excel') || contentType.includes('spreadsheet')) {
          extension = '.xlsx';
        } else if (contentType.includes('csv')) {
          extension = '.csv';
        } else if (contentType.includes('zip')) {
          extension = '.zip';
        }
      }

      const filename = `${reportName}${extension}`;

      // Create download link with better cross-browser support
      const url_obj = window.URL.createObjectURL(correctedBlob);
      const link = document.createElement('a');
      link.href = url_obj;
      link.download = filename;
      link.style.display = 'none'; // Hide the link element
      
      // Append to body, click, and remove
      document.body.appendChild(link);
      link.click();
      
      // Clean up after a short delay to ensure download starts
      setTimeout(() => {
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url_obj);
      }, 100);

      console.log(`Successfully initiated download of ${filename} (${blob.size} bytes)`);
      
      // Return success info
      return {
        success: true,
        filename,
        size: blob.size,
        contentType
      };

    } catch (err) {
      console.error('Download error details:', {
        message: err.message,
        stack: err.stack,
        customerId,
        reportType,
        domains
      });
      
      // Set user-friendly error messages
      let errorMessage = 'Failed to download report';
      
      if (err.message.includes('fetch') || err.message.includes('network') || err.message.includes('NetworkError')) {
        errorMessage = 'Network error. Please check your connection and try again.';
      } else if (err.message.includes('Customer ID')) {
        errorMessage = 'Session error. Please refresh the page and try again.';
      } else if (err.message.includes('Customer data not found')) {
        errorMessage = 'Customer data not found. Please contact support.';
      } else if (err.message) {
        errorMessage = err.message;
      }
      
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  // Clear error function for UI
  const clearError = () => {
    setError(null);
  };

  // Test connection to the reports endpoint
  const testReportsEndpoint = async (customerId) => {
    try {
      const response = await fetch(`https://gnss5bq5km.us-east-2.awsapprunner.com/api/customer/${customerId}/info`);
      return {
        success: response.ok,
        status: response.status,
        message: response.ok ? 'Reports endpoint accessible' : `HTTP ${response.status}`
      };
    } catch (error) {
      return {
        success: false,
        status: 0,
        message: error.message
      };
    }
  };

  return { 
    isLoading, 
    error, 
    downloadReport, 
    clearError, 
    testReportsEndpoint 
  };
};