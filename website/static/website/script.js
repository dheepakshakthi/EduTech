// Switch between forms
function switchToSignup() {
    document.getElementById('loginForm').classList.add('hidden');
    document.getElementById('signupForm').classList.remove('hidden');
    clearErrors();
}

function switchToLogin() {
    document.getElementById('signupForm').classList.add('hidden');
    document.getElementById('loginForm').classList.remove('hidden');
    clearErrors();
}

function clearErrors() {
    document.querySelectorAll('.error').forEach(error => error.textContent = '');
    document.querySelectorAll('input').forEach(input => input.value = '');
}

// Handle Valid Email 
function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// Login Form with Django Backend Integration
document.getElementById('loginFormSubmit').addEventListener('submit', function(e) {
    e.preventDefault();

    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value.trim();
    const emailError = document.getElementById('loginEmailError');
    const passwordError = document.getElementById('loginPasswordError');

    // Clear previous errors
    emailError.textContent = '';
    passwordError.textContent = '';

    // Initialize isValid to true
    let isValid = true;

    // Validation
    if (email === '') {
        emailError.textContent = 'Email is required';
        isValid = false;
    } else if (!isValidEmail(email)) {
        emailError.textContent = 'Please enter a valid email address';
        isValid = false;
    }

    if (password === '') {
        passwordError.textContent = 'Password is required';
        isValid = false;
    } else if (password.length < 6) {
        passwordError.textContent = 'Password must be at least 6 characters';
        isValid = false;
    }

    // Only send to backend if client-side validation passes
    if (isValid) {
        // Send data to Django Backend
        fetch('/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: email, password: password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message); // "Login successful!"
                window.location.reload(); // Or redirect to dashboard
            } else {
                // Show error from backend (e.g., "Invalid email or password")
                alert(data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    }
});

// Signup Form with Django Backend Integration
document.getElementById('signupFormSubmit').addEventListener('submit', function(e) {
    e.preventDefault();

    const email = document.getElementById('signupEmail').value.trim();
    const password = document.getElementById('signupPassword').value.trim();
    const confirmPassword = document.getElementById('confirmPassword').value.trim();
    const emailError = document.getElementById('signupEmailError');
    const passwordError = document.getElementById('signupPasswordError');
    const confirmPasswordError = document.getElementById('confirmPasswordError');

    // Clear previous errors
    emailError.textContent = '';
    passwordError.textContent = '';
    confirmPasswordError.textContent = '';

    // Initialize isValid to true
    let isValid = true;

    // Validation
    if (email === '') {
        emailError.textContent = 'Email is required';
        isValid = false;
    } else if (!isValidEmail(email)) {
        emailError.textContent = 'Please enter a valid email address';
        isValid = false;
    }

    if (password === '') {
        passwordError.textContent = 'Password is required';
        isValid = false;
    } else if (password.length < 6) {
        passwordError.textContent = 'Password must be at least 6 characters';
        isValid = false;
    }

    if (confirmPassword === '') {
        confirmPasswordError.textContent = 'Please confirm your password';
        isValid = false;
    } else if (password !== confirmPassword) {
        confirmPasswordError.textContent = 'Passwords do not match';
        isValid = false;
    }

    // Only send to backend if client-side validation passes
    if (isValid) {
        // Send data to Django Backend
        fetch('/api/signup/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                email: email, 
                password: password,
                name: "New User" // You can add a name field to your HTML later
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Only show success message if backend confirms user was created
                alert(data.message);
                switchToLogin();
                document.getElementById('signupFormSubmit').reset();
            } else {
                // Show error from backend (e.g., "Email already registered")
                alert(data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    }
});