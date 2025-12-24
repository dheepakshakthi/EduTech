// Check URL parameters to determine which form to show
const urlParams = new URLSearchParams(window.location.search);
const mode = urlParams.get('mode');

if (mode === 'signup') {
    switchToSignup();
} else {
    switchToSignin();
}

// Switch between forms
function switchToSignup() {
    document.getElementById('signinForm').classList.add('hidden');
    document.getElementById('signupForm').classList.remove('hidden');
    clearErrors();
}

function switchToSignin() {
    document.getElementById('signupForm').classList.add('hidden');
    document.getElementById('signinForm').classList.remove('hidden');
    clearErrors();
}

function clearErrors() {
    document.querySelectorAll('.error').forEach(error => error.textContent = '');
    document.querySelectorAll('input').forEach(input => {
        if (input.type !== 'checkbox') {
            input.value = '';
        }
    });
    const passwordStrength = document.getElementById('passwordStrength');
    const passwordStrengthText = document.getElementById('passwordStrengthText');
    if (passwordStrength) {
        passwordStrength.className = 'password-strength';
    }
    if (passwordStrengthText) {
        passwordStrengthText.textContent = '';
    }
}

// Email validation
function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// Password strength checker
function checkPasswordStrength(password) {
    const strengthBar = document.getElementById('passwordStrength');
    const strengthText = document.getElementById('passwordStrengthText');
    
    if (!strengthBar || !strengthText) return;
    
    if (password.length === 0) {
        strengthBar.className = 'password-strength';
        strengthText.textContent = '';
        return;
    }

    let strength = 0;
    
    if (password.length >= 8) strength++;
    if (password.length >= 12) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^a-zA-Z0-9]/.test(password)) strength++;
    
    if (strength <= 2) {
        strengthBar.className = 'password-strength weak';
        strengthText.textContent = 'Weak password';
    } else if (strength <= 4) {
        strengthBar.className = 'password-strength medium';
        strengthText.textContent = 'Medium password';
    } else {
        strengthBar.className = 'password-strength strong';
        strengthText.textContent = 'Strong password';
    }
}

// Add event listener for password strength in signup
const signupPasswordInput = document.getElementById('signupPassword');
if (signupPasswordInput) {
    signupPasswordInput.addEventListener('input', function() {
        checkPasswordStrength(this.value);
    });
}

// Sign In Form Handler - with Backend Integration
const signinForm = document.getElementById('signinFormSubmit');
if (signinForm) {
    signinForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const email = document.getElementById('signinEmail').value.trim();
        const password = document.getElementById('signinPassword').value.trim();
        const emailError = document.getElementById('signinEmailError');
        const passwordError = document.getElementById('signinPasswordError');
        
        emailError.textContent = '';
        passwordError.textContent = '';
        
        let isValid = true;

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

        if (isValid) {
            try {
                const response = await fetch('/api/login/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email: email,
                        password: password
                    })
                });

                const data = await response.json();

                if (data.success) {
                    // Store user info in sessionStorage
                    sessionStorage.setItem('user', JSON.stringify({
                        email: email,
                        name: data.user,
                        loginTime: new Date().toISOString()
                    }));
                    
                    // Store email in localStorage for chat persistence
                    localStorage.setItem('userEmail', email);
                    
                    // Redirect to dashboard
                    window.location.href = '/dashboard/';
                } else {
                    passwordError.textContent = data.message || 'Invalid email or password';
                }
            } catch (error) {
                console.error('Login error:', error);
                passwordError.textContent = 'An error occurred. Please try again.';
            }
        }
    });
}

// Sign Up Form Handler - with Backend Integration
const signupForm = document.getElementById('signupFormSubmit');
if (signupForm) {
    signupForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const firstName = document.getElementById('firstName').value.trim();
        const lastName = document.getElementById('lastName').value.trim();
        const email = document.getElementById('signupEmail').value.trim();
        const age = document.getElementById('age').value.trim();
        const password = document.getElementById('signupPassword').value.trim();
        const confirmPassword = document.getElementById('confirmPassword').value.trim();
        
        const firstNameError = document.getElementById('firstNameError');
        const lastNameError = document.getElementById('lastNameError');
        const emailError = document.getElementById('signupEmailError');
        const ageError = document.getElementById('ageError');
        const passwordError = document.getElementById('signupPasswordError');
        const confirmPasswordError = document.getElementById('confirmPasswordError');
        
        // Clear previous errors
        firstNameError.textContent = '';
        lastNameError.textContent = '';
        emailError.textContent = '';
        ageError.textContent = '';
        passwordError.textContent = '';
        confirmPasswordError.textContent = '';
        
        let isValid = true;

        // Validate first name
        if (firstName === '') {
            firstNameError.textContent = 'First name is required';
            isValid = false;
        } else if (firstName.length < 2) {
            firstNameError.textContent = 'First name must be at least 2 characters';
            isValid = false;
        }

        // Validate last name
        if (lastName === '') {
            lastNameError.textContent = 'Last name is required';
            isValid = false;
        } else if (lastName.length < 2) {
            lastNameError.textContent = 'Last name must be at least 2 characters';
            isValid = false;
        }

        // Validate email
        if (email === '') {
            emailError.textContent = 'Email is required';
            isValid = false;
        } else if (!isValidEmail(email)) {
            emailError.textContent = 'Please enter a valid email address';
            isValid = false;
        }

        // Validate age
        if (age === '') {
            ageError.textContent = 'Age is required';
            isValid = false;
        } else if (parseInt(age) < 13) {
            ageError.textContent = 'You must be at least 13 years old';
            isValid = false;
        } else if (parseInt(age) > 120) {
            ageError.textContent = 'Please enter a valid age';
            isValid = false;
        }

        // Validate password
        if (password === '') {
            passwordError.textContent = 'Password is required';
            isValid = false;
        } else if (password.length < 6) {
            passwordError.textContent = 'Password must be at least 6 characters';
            isValid = false;
        }

        // Validate confirm password
        if (confirmPassword === '') {
            confirmPasswordError.textContent = 'Please confirm your password';
            isValid = false;
        } else if (password !== confirmPassword) {
            confirmPasswordError.textContent = 'Passwords do not match';
            isValid = false;
        }

        if (isValid) {
            try {
                const response = await fetch('/api/signup/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        name: `${firstName} ${lastName}`,
                        email: email,
                        password: password
                    })
                });

                const data = await response.json();

                if (data.success) {
                    // Store user info in sessionStorage
                    sessionStorage.setItem('user', JSON.stringify({
                        firstName: firstName,
                        lastName: lastName,
                        email: email,
                        name: `${firstName} ${lastName}`,
                        registrationDate: new Date().toISOString()
                    }));
                    
                    alert('Account created successfully! Redirecting to dashboard...');
                    
                    // Redirect to dashboard
                    window.location.href = '/dashboard/';
                } else {
                    emailError.textContent = data.message || 'Failed to create account';
                }
            } catch (error) {
                console.error('Signup error:', error);
                emailError.textContent = 'An error occurred. Please try again.';
            }
        }
    });
}
