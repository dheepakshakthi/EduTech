// Check if user is logged in
document.addEventListener('DOMContentLoaded', function() {
    const storedUser = sessionStorage.getItem('user');
    
    if (!storedUser) {
        // Redirect to auth page if not logged in
        alert('Please sign in to access the dashboard');
        window.location.href = '/auth/';
        return;
    }
    
    // Parse user data and display
    const userData = JSON.parse(storedUser);
    displayUserInfo(userData);
    drawProgressChart();
});

// Display user information
function displayUserInfo(userData) {
    const userName = document.getElementById('userName');
    const userEmail = document.getElementById('userEmail');
    
    if (userData) {
        if (userName) {
            userName.textContent = userData.name || userData.firstName || 'User';
        }
        if (userEmail) {
            userEmail.textContent = userData.email || 'user@example.com';
        }
    }
}

// Logout function
function logout() {
    if (confirm('Are you sure you want to logout?')) {
        // Clear user data from sessionStorage
        sessionStorage.removeItem('user');
        
        // Redirect to home page
        window.location.href = '/';
    }
}

// Draw progress chart (simple wave chart)
function drawProgressChart() {
    const canvas = document.getElementById('progressChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    canvas.width = 300;
    canvas.height = 150;
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw wave
    ctx.beginPath();
    ctx.strokeStyle = '#667EEA';
    ctx.lineWidth = 3;
    
    const amplitude = 30;
    const frequency = 0.02;
    const yOffset = canvas.height / 2;
    
    for (let x = 0; x < canvas.width; x++) {
        const y = yOffset + amplitude * Math.sin(frequency * x);
        
        if (x === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    }
    
    ctx.stroke();
    
    // Animate the wave
    let offset = 0;
    function animateWave() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.beginPath();
        ctx.strokeStyle = '#667EEA';
        ctx.lineWidth = 3;
        
        for (let x = 0; x < canvas.width; x++) {
            const y = yOffset + amplitude * Math.sin(frequency * x + offset);
            
            if (x === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        }
        
        ctx.stroke();
        offset += 0.05;
        
        requestAnimationFrame(animateWave);
    }
    
    animateWave();
}
