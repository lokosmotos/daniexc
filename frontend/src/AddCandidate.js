import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function AddCandidate() {
  const [form, setForm] = useState({
    name: '',
    position: 'Groomer',
    branch: 'Main',
    resume: null,
    no_resume_reason: ''
  });
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/candidates', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      });
      if (response.ok) navigate('/pool');
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="form-container">
      <h2>😸 Add New Candidate</h2>
      <form onSubmit={handleSubmit}>
        {/* Form fields from previous example */}
        <button type="submit" className="cat-button">Save</button>
      </form>
    </div>
  );
}
