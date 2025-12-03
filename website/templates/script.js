// Login Form Handler
const loginForm = document.getElementById("loginForm");
if (loginForm) {
    loginForm.addEventListener("submit", function (e) {
        e.preventDefault();

        let email = document.getElementById("email").value.trim();
        let password = document.getElementById("password").value.trim();

        let emailError = document.getElementById("emailError");
        let passwordError = document.getElementById("passwordError");

        emailError.textContent = "";
        passwordError.textContent = "";

        let isValid = true;

        if (email === "") {
            emailError.textContent = "Email is required";
            isValid = false;
        } else if (!/^\S+@\S+\.\S+$/.test(email)) {
            emailError.textContent = "Enter a valid email address";
            isValid = false;
        }

        if (password === "") {
            passwordError.textContent = "Password is required";
            isValid = false;
        }

        if (isValid) {
            alert("Login successful!");
        }
    });
}

// Signup Form Handler
const signupForm = document.getElementById("signupForm");
if (signupForm) {
    signupForm.addEventListener("submit", function (e) {
        e.preventDefault();

        let email = document.getElementById("signupEmail").value.trim();
        let password = document.getElementById("signupPassword").value.trim();

        let emailError = document.getElementById("signupEmailError");
        let passwordError = document.getElementById("signupPasswordError");

        emailError.textContent = "";
        passwordError.textContent = "";

        let isValid = true;

        if (email === "") {
            emailError.textContent = "Email is required";
            isValid = false;
        } else if (!/^\S+@\S+\.\S+$/.test(email)) {
            emailError.textContent = "Enter a valid email address";
            isValid = false;
        }

        if (password === "") {
            passwordError.textContent = "Password is required";
            isValid = false;
        }

        if (isValid) {
            alert("Account created successfully!");
        }
    });
}

