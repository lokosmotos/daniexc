// frontend/src/components/MessagingTemplates.js
import React, { useState } from 'react';

const templates = {
  Interview: [
    {
      title: "Interview Invitation",
      message: `Hi {Name}, you're invited to an interview for the {Position} role at our {Branch} branch.
📍 Address: {BranchAddress}
📅 Date: {Date}
⏰ Time: {Time}

Please reply to confirm. Thank you!`,
    },
    {
      title: "Interview Reminder",
      message: `Hi {Name}, friendly reminder: your interview for the {Position} role is tomorrow at {Time}, {Branch}.
Please reply YES to confirm attendance.`,
    },
  ],
  JobOffer: [
    {
      title: "Job Offer",
      message: `Congratulations {Name}, you're selected for the {Position} role at {Branch}! 🎉
Please reply YES to accept this offer and start on {StartDate}.`,
    },
    {
      title: "First-Day Instructions",
      message: `Welcome to the team, {Name}! 💼
Your first day is {StartDate} at {Time}. Please wear a black t-shirt and bring your IC.

📍 Location: {BranchAddress}
Let us know if you need help finding the place.`,
    },
  ],
  Training: [
    {
      title: "Training Reminder",
      message: `Hi {Name}, reminder: your training is scheduled for {Date} at {Time} at {Branch}.
Please reply YES to confirm.`,
    },
    {
      title: "No-Show for Training",
      message: `Hi {Name}, we noticed you didn’t attend the training at {Branch}.
If you're still interested, please reply and we’ll try to reschedule.`,
    },
  ],
};

const MessagingTemplates = () => {
  const [search, setSearch] = useState('');

  const filteredTemplates = Object.entries(templates).reduce((acc, [category, messages]) => {
    const filtered = messages.filter(({ title, message }) =>
      title.toLowerCase().includes(search.toLowerCase()) ||
      message.toLowerCase().includes(search.toLowerCase())
    );
    if (filtered.length) acc[category] = filtered;
    return acc;
  }, {});

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    alert('Message copied!');
  };

  return (
    <div className="p-6">
      <h1 className="text-xl font-bold mb-4">📨 Messaging Templates</h1>
      <input
        className="p-2 border rounded mb-6 w-full"
        placeholder="Search templates..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
      {Object.entries(filteredTemplates).map(([category, messages]) => (
        <div key={category} className="mb-6">
          <h2 className="text-lg font-semibold mb-2">{category}</h2>
          {messages.map(({ title, message }) => (
            <div key={title} className="bg-white border p-4 mb-3 rounded shadow-sm">
              <strong>{title}</strong>
              <pre className="whitespace-pre-wrap text-sm mt-2">{message}</pre>
              <button
                className="mt-2 text-blue-600 hover:underline text-sm"
                onClick={() => copyToClipboard(message)}
              >
                Copy to Clipboard
              </button>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
};

export default MessagingTemplates;
