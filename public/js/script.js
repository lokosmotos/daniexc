// Database simulation (in a real app, you'd use a proper database)
let candidates = JSON.parse(localStorage.getItem('candidates')) || [];

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    const path = window.location.pathname;
    
    if (path === '/' || path === '/index.html') {
        initHomePage();
    } else if (path === '/add-candidate.html') {
        initAddCandidatePage();
    } else if (path === '/pool.html') {
        initCandidatePoolPage();
    } else if (path === '/edit-candidate.html') {
        initEditCandidatePage();
    }
});

// Home Page Functions
function initHomePage() {
    updateDashboardStats();
}

function updateDashboardStats() {
    const totalCandidates = candidates.length;
    const activeCandidates = candidates.filter(c => c.status !== 'Hired' && c.status !== 'Rejected').length;
    const hiredThisMonth = candidates.filter(c => 
        c.status === 'Hired' && 
        new Date(c.updatedAt).getMonth() === new Date().getMonth()
    ).length;
    
    document.getElementById('total-candidates').textContent = totalCandidates;
    document.getElementById('active-candidates').textContent = activeCandidates;
    document.getElementById('hired-candidates').textContent = hiredThisMonth;
}

// Add Candidate Page Functions
function initAddCandidatePage() {
    const form = document.getElementById('candidate-form');
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const newCandidate = {
            id: Date.now().toString(),
            fullName: document.getElementById('fullName').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            position: document.getElementById('position').value,
            skills: document.getElementById('skills').value.split(',').map(skill => skill.trim()),
            status: document.getElementById('status').value,
            notes: document.getElementById('notes').value,
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString()
        };
        
        candidates.push(newCandidate);
        saveCandidates();
        
        alert('Candidate added successfully!');
        form.reset();
    });
}

// Candidate Pool Page Functions
function initCandidatePoolPage() {
    renderCandidatesTable();
    setupFilters();
}

function renderCandidatesTable() {
    const tableBody = document.querySelector('#candidates-table tbody');
    tableBody.innerHTML = '';
    
    // Populate position filter
    const positionFilter = document.getElementById('position-filter');
    const positions = [...new Set(candidates.map(c => c.position))];
    positions.forEach(position => {
        const option = document.createElement('option');
        option.value = position;
        option.textContent = position;
        positionFilter.appendChild(option);
    });
    
    candidates.forEach(candidate => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${candidate.fullName}</td>
            <td>${candidate.email}</td>
            <td>${candidate.phone || 'N/A'}</td>
            <td>${candidate.position}</td>
            <td>${candidate.skills.join(', ')}</td>
            <td class="status-${candidate.status.toLowerCase()}">${candidate.status}</td>
            <td>
                <a href="/edit-candidate.html?id=${candidate.id}" class="btn btn-sm btn-primary">Edit</a>
            </td>
        `;
        tableBody.appendChild(row);
    });
    
    // Initialize DataTable
    $('#candidates-table').DataTable({
        responsive: true
    });
}

function setupFilters() {
    const searchInput = document.getElementById('search-input');
    const statusFilter = document.getElementById('status-filter');
    const positionFilter = document.getElementById('position-filter');
    
    function applyFilters() {
        const searchTerm = searchInput.value.toLowerCase();
        const statusValue = statusFilter.value;
        const positionValue = positionFilter.value;
        
        const filtered = candidates.filter(candidate => {
            const matchesSearch = 
                candidate.fullName.toLowerCase().includes(searchTerm) ||
                candidate.email.toLowerCase().includes(searchTerm) ||
                candidate.position.toLowerCase().includes(searchTerm) ||
                candidate.skills.some(skill => skill.toLowerCase().includes(searchTerm));
            
            const matchesStatus = statusValue ? candidate.status === statusValue : true;
            const matchesPosition = positionValue ? candidate.position === positionValue : true;
            
            return matchesSearch && matchesStatus && matchesPosition;
        });
        
        // Re-render table with filtered results
        renderFilteredCandidates(filtered);
    }
    
    searchInput.addEventListener('input', applyFilters);
    statusFilter.addEventListener('change', applyFilters);
    positionFilter.addEventListener('change', applyFilters);
}

function renderFilteredCandidates(filteredCandidates) {
    const tableBody = document.querySelector('#candidates-table tbody');
    tableBody.innerHTML = '';
    
    filteredCandidates.forEach(candidate => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${candidate.fullName}</td>
            <td>${candidate.email}</td>
            <td>${candidate.phone || 'N/A'}</td>
            <td>${candidate.position}</td>
            <td>${candidate.skills.join(', ')}</td>
            <td class="status-${candidate.status.toLowerCase()}">${candidate.status}</td>
            <td>
                <a href="/edit-candidate.html?id=${candidate.id}" class="btn btn-sm btn-primary">Edit</a>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

// Edit Candidate Page Functions
function initEditCandidatePage() {
    const urlParams = new URLSearchParams(window.location.search);
    const candidateId = urlParams.get('id');
    const candidate = candidates.find(c => c.id === candidateId);
    
    if (!candidate) {
        alert('Candidate not found!');
        window.location.href = '/pool.html';
        return;
    }
    
    // Populate form with candidate data
    document.getElementById('candidate-id').value = candidate.id;
    document.getElementById('edit-fullName').value = candidate.fullName;
    document.getElementById('edit-email').value = candidate.email;
    document.getElementById('edit-phone').value = candidate.phone || '';
    document.getElementById('edit-position').value = candidate.position;
    document.getElementById('edit-skills').value = candidate.skills.join(', ');
    document.getElementById('edit-status').value = candidate.status;
    document.getElementById('edit-notes').value = candidate.notes || '';
    
    // Setup form submit
    const form = document.getElementById('edit-candidate-form');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const updatedCandidate = {
            ...candidate,
            fullName: document.getElementById('edit-fullName').value,
            email: document.getElementById('edit-email').value,
            phone: document.getElementById('edit-phone').value,
            position: document.getElementById('edit-position').value,
            skills: document.getElementById('edit-skills').value.split(',').map(skill => skill.trim()),
            status: document.getElementById('edit-status').value,
            notes: document.getElementById('edit-notes').value,
            updatedAt: new Date().toISOString()
        };
        
        const index = candidates.findIndex(c => c.id === candidateId);
        candidates[index] = updatedCandidate;
        saveCandidates();
        
        alert('Candidate updated successfully!');
        window.location.href = '/pool.html';
    });
    
    // Setup delete button
    document.getElementById('delete-candidate').addEventListener('click', function() {
        if (confirm('Are you sure you want to delete this candidate?')) {
            candidates = candidates.filter(c => c.id !== candidateId);
            saveCandidates();
            alert('Candidate deleted successfully!');
            window.location.href = '/pool.html';
        }
    });
}

// Helper function to save candidates to localStorage
function saveCandidates() {
    localStorage.setItem('candidates', JSON.stringify(candidates));
}