import React from 'react';
import './ProcessingDot.css'; // Import your custom CSS

const ProcessingDot = () => {
  return (
    <div style={{ display: 'inline-flex', alignItems: 'center' }}>
      <div className="processing-dot"></div>
      &nbsp; 
      Processing...
    </div>
  );
};

export default ProcessingDot;