import React, { useEffect, useState } from 'react';

const Dashboard = ({ user }) => {
  const [candidates, setCandidates] = useState([]);

  useEffect(() => {
    fetch("https://daniexc.onrender.com/candidates")
      .then(res => res.json())
      .then(data => setCandidates(data))
      .catch(err => console.error("Failed to fetch candidates:", err));
  }, []);

  const hired = candidates.filter(c => c.status === "Hired").length;
  const scheduled = candidates.filter(c => c.status === "Interview Scheduled").length;

  return (
    <div className="dashboard">
      <h2>Welcome, {user.name}</h2>

      <div className="stats">
        <p><strong>Total Candidates:</strong> {candidates.length}</p>
        <p><strong>Hired:</strong> {hired}</p>
        <p><strong>Scheduled:</strong> {scheduled}</p>
      </div>

      <h3>Candidate List</h3>
      <ul>
        {candidates.map((c) => (
          <li key={c.id}>
            {c.name} — <span>{c.status}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Dashboard;
