import React, { useState, useEffect } from 'react';

const CandidatePool = () => {
  const [candidates, setCandidates] = useState([]);

  useEffect(() => {
    // Fetch candidate data (e.g., from backend API)
    setCandidates([
      { id: 1, name: 'John Doe', status: 'Hired' },
      { id: 2, name: 'Jane Smith', status: 'Interview Scheduled' },
    ]);
  }, []);

  return (
    <div className="candidate-pool">
      <h2>Candidate Pool</h2>
      <ul>
        {candidates.map((candidate) => (
          <li key={candidate.id}>
            {candidate.name} - <span>{candidate.status}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CandidatePool;
