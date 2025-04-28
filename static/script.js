document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("login-form");
    const signupForm = document.getElementById("signup-form");
    const signupContainer = document.getElementById("signup-container");
    const loginContainer = document.querySelector(".container");
    const loginErrorMsg = document.getElementById("login-error-message");
    const signupErrorMsg = document.getElementById("signup-error-message");
    
    // Check if user is already logged in
    const checkLoginStatus = async () => {
        try {
            const response = await fetch("/check_session", {
                method: "GET",
                credentials: "include"
            });
            const data = await response.json();
            const currentPath = window.location.pathname;
            if (data.isLoggedIn) {
                if (data.userType === "clerk" && currentPath !== "/clerk") {
                    window.location.href = "/clerk";
                } else if (data.userType !== "clerk" && currentPath !== "/") {
                    window.location.href = "/";
                }
            } else if (currentPath !== "/login") {
                window.location.href = "/login";
            }
        } catch (error) {
            console.error("Session check failed:", error);
        }
    };
    
    // Run on page load
    checkLoginStatus();
    document.getElementById("logout-btn")?.addEventListener("click", () => {
        localStorage.removeItem("user");
        fetch("/logout").then(() => window.location.href = "/login");
    });
    // Toggle between login and signup forms
    document.getElementById("show-signup").addEventListener("click", (e) => {
        e.preventDefault();
        loginContainer.classList.add("hidden");
        signupContainer.classList.remove("hidden");
    });

    document.getElementById("show-login").addEventListener("click", (e) => {
        e.preventDefault();
        signupContainer.classList.add("hidden");
        loginContainer.classList.remove("hidden");
    });

   // In script.js, modify the login form submit handler
loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;
    console.log("Login attempt:", username);

    try {
        // Use JSON format instead of FormData
        const response = await fetch("/verify_login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password }),
            credentials: "include"
        });

        const data = await response.json();
        console.log("Login response:", data);
        
        if (data.success) {
            localStorage.setItem("user", JSON.stringify({
                username: username,
                customer_name: data.customer_name || "Clerk",
                userType: data.user_type || "customer",
                isLoggedIn: true
            }));
            window.location.href = data.redirect;
        } else {
            displayError(loginErrorMsg, data.message || "Login failed. Please try again.");
        }
    } catch (error) {
        console.error("Login error:", error);
        displayError(loginErrorMsg, "Network error. Please try again later.");
    }
});
    
    // Signup form handler
    if (signupForm) {
        signupForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const username = document.getElementById("signup-username").value.trim();
            const password = document.getElementById("signup-password").value;
            const confirmPassword = document.getElementById("signup-confirm-password").value;
            const name = document.getElementById("signup-name").value.trim();
            const phone = document.getElementById("signup-phone").value.trim();
            const email = document.getElementById("signup-email").value.trim();
            const address = document.getElementById("signup-address").value.trim();

            // Basic validation
            if (!username || !password || !name || !email || !address) {
                displayError(signupErrorMsg, "Please fill in all required fields");
                return;
            }
            
            // Validate email format
            if (!isValidEmail(email)) {
                displayError(signupErrorMsg, "Please enter a valid email address");
                return;
            }

            // Password validation
            if (password.length < 6) {
                displayError(signupErrorMsg, "Password must be at least 6 characters long");
                return;
            }
            
            // Check if passwords match
            if (password !== confirmPassword) {
                displayError(signupErrorMsg, "Passwords do not match!");
                return;
            }

            try {
                const response = await fetch("/add_customer", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        username: username,
                        passwd: password,
                        customer_name: name,
                        contact_info: phone,
                        customer_address: address,
                        email: email
                    }),
                });

                const data = await response.json();
                console.log("Signup response:", data);

                if (response.ok) {
                    alert("Account created successfully! Please log in.");
                    // Clear form
                    signupForm.reset();
                    // Switch to login form
                    signupContainer.classList.add("hidden");
                    loginContainer.classList.remove("hidden");
                } else {
                    // Handle different error cases
                    if (data.error === "username_exists") {
                        displayError(signupErrorMsg, "Username already exists. Please choose another.");
                    } else {
                        displayError(signupErrorMsg, data.message || "Signup failed. Please try again.");
                    }
                }
            } catch (error) {
                console.error("Signup error:", error);
                displayError(signupErrorMsg, "Server error. Please try again later.");
            }
        });
    }

    // Helper function to display error messages
    function displayError(element, message) {
        if (!element) return;
        element.textContent = message;
        element.style.display = "block";
        element.style.color = "red";
        element.style.marginTop = "10px";
        
        // Hide error after 5 seconds
        setTimeout(() => {
            element.style.display = "none";
        }, 5000);
    }
    
    // Helper function to validate email format
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
});


  