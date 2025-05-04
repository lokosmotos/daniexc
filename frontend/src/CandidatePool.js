import BulkMessaging from './components/BulkMessaging';

export default function CandidatePool() {
  const [candidates, setCandidates] = useState([]);
  const [showMessaging, setShowMessaging] = useState(false);

  useEffect(() => {
    fetch('/candidates')
      .then(res => res.json())
      .then(setCandidates);
  }, []);

  return (
    <div className="pool-container">
      <div className="pool-header">
        <h2>Candidate Pool ({candidates.length})</h2>
        <button onClick={() => setShowMessaging(!showMessaging)}>
          {showMessaging ? 'Hide' : 'Show'} Messaging
        </button>
      </div>

      {showMessaging && <BulkMessaging candidates={candidates} />}

      <div className="filters">
        {/* ... existing filters ... */}
      </div>

      <table className="candidate-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Position</th>
            <th>Resume</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {candidates.map(candidate => (
            <tr key={candidate.id}>
              <td>{candidate.name}</td>
              <td>{candidate.position}</td>
              <td>
                {candidate.resume_url ? (
                  <a href={candidate.resume_url} target="_blank">
                    <img src="/assets/resume-icon.png" width="20" />
                  </a>
                ) : (
                  <span className="reason">{candidate.no_resume_reason}</span>
                )}
              </td>
              <td>{candidate.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
