const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.static('public'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'views', 'home.html'));
});

app.get('/add-candidate', (req, res) => {
    res.sendFile(path.join(__dirname, 'views', 'add-candidate.html'));
});

app.get('/pool', (req, res) => {
    res.sendFile(path.join(__dirname, 'views', 'pool.html'));
});

app.get('/edit-candidate', (req, res) => {
    res.sendFile(path.join(__dirname, 'views', 'edit-candidate.html'));
});

// API Routes
const DATA_FILE = path.join(__dirname, 'data', 'candidates.json');

// Ensure data directory exists
if (!fs.existsSync(path.join(__dirname, 'data'))) {
    fs.mkdirSync(path.join(__dirname, 'data'));
}

// Ensure data file exists
if (!fs.existsSync(DATA_FILE)) {
    fs.writeFileSync(DATA_FILE, '[]');
}

app.get('/api/candidates', (req, res) => {
    fs.readFile(DATA_FILE, 'utf8', (err, data) => {
        if (err) {
            return res.status(500).json({ error: 'Error reading data' });
        }
        res.json(JSON.parse(data));
    });
});

app.post('/api/candidates', (req, res) => {
    const newCandidate = {
        id: Date.now().toString(),
        ...req.body,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
    };
    
    fs.readFile(DATA_FILE, 'utf8', (err, data) => {
        if (err) {
            return res.status(500).json({ error: 'Error reading data' });
        }
        
        const candidates = JSON.parse(data);
        candidates.push(newCandidate);
        
        fs.writeFile(DATA_FILE, JSON.stringify(candidates, null, 2), (err) => {
            if (err) {
                return res.status(500).json({ error: 'Error saving data' });
            }
            res.status(201).json(newCandidate);
        });
    });
});

app.put('/api/candidates/:id', (req, res) => {
    const { id } = req.params;
    
    fs.readFile(DATA_FILE, 'utf8', (err, data) => {
        if (err) {
            return res.status(500).json({ error: 'Error reading data' });
        }
        
        let candidates = JSON.parse(data);
        const index = candidates.findIndex(c => c.id === id);
        
        if (index === -1) {
            return res.status(404).json({ error: 'Candidate not found' });
        }
        
        candidates[index] = {
            ...candidates[index],
            ...req.body,
            updatedAt: new Date().toISOString()
        };
        
        fs.writeFile(DATA_FILE, JSON.stringify(candidates, null, 2), (err) => {
            if (err) {
                return res.status(500).json({ error: 'Error saving data' });
            }
            res.json(candidates[index]);
        });
    });
});

app.delete('/api/candidates/:id', (req, res) => {
    const { id } = req.params;
    
    fs.readFile(DATA_FILE, 'utf8', (err, data) => {
        if (err) {
            return res.status(500).json({ error: 'Error reading data' });
        }
        
        let candidates = JSON.parse(data);
        candidates = candidates.filter(c => c.id !== id);
        
        fs.writeFile(DATA_FILE, JSON.stringify(candidates, null, 2), (err) => {
            if (err) {
                return res.status(500).json({ error: 'Error saving data' });
            }
            res.json({ message: 'Candidate deleted successfully' });
        });
    });
});

// Start server
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});