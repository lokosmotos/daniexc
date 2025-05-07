import React, { useState } from 'react';

const AddCandidate = () => {
  const [candidate, setCandidate] = useState({
    name: '',
    position: '',
    branch: '',
    resume: null,
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCandidate((prev) => ({ ...prev, [name]: value }));
  };

  const handleResumeUpload = (e) => {
    setCandidate({ ...candidate, resume: e.target.files[0] });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Submit candidate data (e.g., POST request to backend)
    console.log(candidate);
  };

  return (
    <div className="add-candidate-form">
      <h2>Add New Candidate</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="name"
          value={candidate.name}
          onChange={handleChange}
          placeholder="Candidate Name"
          required
        />
        <input
          type="text"
          name="position"
          value={candidate.position}
          onChange={handleChange}
          placeholder="Position"
          required
        />
        <input
          type="text"
          name="branch"
          value={candidate.branch}
          onChange={handleChange}
          placeholder="Branch"
          required
        />
        <input
          type="file"
          name="resume"
          onChange={handleResumeUpload}
          required
        />
        <button type="submit">Add Candidate</button>
      </form>
    </div>
  );
};

export default AddCandidate;
