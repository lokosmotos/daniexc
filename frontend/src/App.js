import { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from './Login';
import Dashboard from './Dashboard';
import AddCandidate from './AddCandidate';
import CandidatePool from './CandidatePool';
import './styles.css';

export default function App() {
  const [user, setUser] = useState(null);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={user ? <Dashboard user={user} /> : <Login setUser={setUser} />} />
        <Route path="/add" element={<AddCandidate />} />
        <Route path="/pool" element={<CandidatePool />} />
      </Routes>
    </BrowserRouter>
  );
}
