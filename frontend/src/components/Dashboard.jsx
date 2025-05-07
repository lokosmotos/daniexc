import React from 'react';

const Dashboard = ({ user }) => {
  return (
    <div className="dashboard">
      <h2>Welcome, {user.name}</h2>
      <p>Quick Stats</p>
      <ul>
        <li>5 interviews this week</li>
        <li>2 urgent groomer openings</li>
        <li>87 total candidates in pool</li>
      </ul>
      <p>Safe Hiring Calculator</p>
      <button>Need 3 staff</button>
    </div>
  );
};

export default Dashboard;
