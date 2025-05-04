export default function ResumeUpload({ value, onChange }) {
  const [isGoogleDrive, setIsGoogleDrive] = useState(true);

  return (
    <div className="resume-section">
      <label>Resume (Google Drive Link)</label>
      <input
        type="url"
        placeholder="https://drive.google.com/..."
        pattern="https://drive.google.com.*"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        required={!isGoogleDrive}
      />
      
      <div className="toggle">
        <label>
          <input 
            type="checkbox" 
            checked={!isGoogleDrive}
            onChange={() => setIsGoogleDrive(!isGoogleDrive)}
          />
          No Resume? Specify Reason
        </label>
      </div>

      {!isGoogleDrive && (
        <select required>
          <option value="">Select reason...</option>
          <option>Will bring physically</option>
          <option>Referred by staff</option>
          <option>Experienced but no resume</option>
        </select>
      )}
    </div>
  );
}
