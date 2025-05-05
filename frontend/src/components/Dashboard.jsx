import { useState, useEffect } from 'react';
import axios from 'axios';
import { Doughnut, Bar } from 'react-chartjs-2';

export default function Dashboard() {
  const [stats, setStats] = useState({
    total: 0,
    hired: 0,
    scheduled: 0
  });

  useEffect(() => {
    axios.get('https://your-render-url.onrender.com/candidates')
      .then(res => {
        const data = res.data;
        setStats({
          total: data.length,
          hired: data.filter(c => c.status === 'Hired').length,
          scheduled: data.filter(c => c.status === 'Scheduled').length
        });
      });
  }, []);

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      {/* Stats Cards */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-gray-500">Total Candidates</h3>
        <p className="text-3xl font-bold">{stats.total}</p>
      </div>
      
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-gray-500">Hired</h3>
        <p className="text-3xl font-bold text-green-600">{stats.hired}</p>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-gray-500">Scheduled</h3>
        <p className="text-3xl font-bold text-blue-600">{stats.scheduled}</p>
      </div>

      {/* Charts */}
      <div className="md:col-span-2 bg-white p-6 rounded-lg shadow">
        <h3 className="mb-4">Hiring Pipeline</h3>
        <Bar data={chartData} options={{ responsive: true }} />
      </div>
    </div>
  );
}
