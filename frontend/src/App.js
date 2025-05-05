import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import CandidateList from './components/CandidateList';
import Sidebar from './components/Sidebar';

function App() {
  return (
    <BrowserRouter>
      <div className="flex h-screen bg-gray-100">
        <Sidebar />
        <div className="flex-1 p-8 overflow-auto">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/candidates" element={<CandidateList />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}
