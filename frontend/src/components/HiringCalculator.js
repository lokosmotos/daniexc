// frontend/src/components/HiringCalculator.js
import React, { useState } from 'react';

const HiringCalculator = () => {
  const [needed, setNeeded] = useState(0);
  const [suggested, setSuggested] = useState(null);

  const handleCalculate = () => {
    const noShowRate = 0.33; // Default no-show rate
    const calcSuggested = Math.ceil(needed / (1 - noShowRate));
    setSuggested(calcSuggested);
  };

  return (
    <div>
      <h3>Safe Hiring Calculator</h3>
      <input 
        type="number" 
        value={needed} 
        onChange={(e) => setNeeded(e.target.value)} 
        placeholder="Enter number of staff needed"
      />
      <button onClick={handleCalculate}>Calculate</button>
      {suggested !== null && (
        <p>You should recruit {suggested} candidates based on a 33% no-show rate.</p>
      )}
    </div>
  );
};

export default HiringCalculator;
