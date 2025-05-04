export default function BulkMessaging({ candidates }) {
  const [selected, setSelected] = useState([]);
  const [messageType, setMessageType] = useState('interview_reminder');

  const sendMessages = async () => {
    const response = await fetch('/send-bulk-messages', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        type: messageType,
        candidate_ids: selected
      })
    });
    
    if (response.ok) alert(`Sent ${selected.length} messages!`);
  };

  return (
    <div className="bulk-messaging">
      <h3>📨 Send Bulk Messages</h3>
      
      <select 
        value={messageType}
        onChange={(e) => setMessageType(e.target.value)}
      >
        <option value="interview_reminder">Interview Reminder</option>
        <option value="no_show">No-Show Follow Up</option>
        <option value="standby">Standby Inquiry</option>
      </select>

      <div className="candidate-list">
        {candidates.map(candidate => (
          <div key={candidate.id}>
            <input
              type="checkbox"
              checked={selected.includes(candidate.id)}
              onChange={() => setSelected(prev => 
                prev.includes(candidate.id)
                  ? prev.filter(id => id !== candidate.id)
                  : [...prev, candidate.id]
              }
            />
            {candidate.name} ({candidate.position})
          </div>
        ))}
      </div>

      <button 
        onClick={sendMessages}
        disabled={selected.length === 0}
      >
        Send to {selected.length} Candidates
      </button>
    </div>
  );
}
