import { useState } from 'react';
import { addCandidate } from '../services/api';

export default function AddCandidateForm() {
  const [form, setForm] = useState({
    full_name: '',
    position_applied: '',
    branch: 'Johor'
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    addCandidate(form)
      .then(() => alert('Candidate added!'));
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-xl font-semibold mb-4">Add New Candidate</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <input
          type="text"
          placeholder="Full Name"
          className="p-2 border rounded"
          value={form.full_name}
          onChange={(e) => setForm({...form, full_name: e.target.value})}
          required
        />
        <select
          className="p-2 border rounded"
          value={form.branch}
          onChange={(e) => setForm({...form, branch: e.target.value})}
        >
          <option value="Johor">Johor</option>
          <option value="Shah Alam">Shah Alam</option>
        </select>
      </div>
      <button
        type="submit"
        className="mt-4 bg-primary text-white py-2 px-4 rounded hover:bg-primary-dark"
      >
        Save Candidate
      </button>
    </form>
  );
}
