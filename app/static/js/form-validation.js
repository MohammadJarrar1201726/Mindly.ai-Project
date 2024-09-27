const validateForm = (event) => {
    event.preventDefault(); 

    const name = document.getElementById("sign-up-name").value.trim();
    const email = document.getElementById("sign-up-email").value.trim();
    const password = document.getElementById("sign-up-password").value.trim();

    const nameError = document.getElementById("name-error");
    const emailError = document.getElementById("email-error");
    const passwordError = document.getElementById("password-error");

    [nameError, emailError, passwordError].forEach(errorElement => errorElement.textContent = "");

    let isValid = true; 

    if (!name) {
        nameError.textContent = "Full Name is required.";
        isValid = false;
    } else if (!/^[a-zA-Z0-9_ ]{3,50}$/.test(name)) {
        nameError.textContent = "Username must be 3-50 characters long and can include letters, numbers, underscores, and spaces.";
        isValid = false;
    }

    if (!email) {
        emailError.textContent = "Email is required.";
        isValid = false;
    } else if (!/^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$/.test(email)) {
        emailError.textContent = "Invalid email format.";
        isValid = false;
    }

    let errors = [];

    if (!password) {
        errors.push("Password is required.");
    } else {
        if (password.length < 8) {
            errors.push("Password must be at least 8 characters long.");
        }
        if (!/\d/.test(password)) {
            errors.push("Password must contain at least one number.");
        }
        if (!/[A-Z]/.test(password)) {
            errors.push("Password must contain at least one uppercase letter.");
        }
        if (!/[a-z]/.test(password)) {
            errors.push("Password must contain at least one lowercase letter.");
        }
        if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
            errors.push("Password must contain at least one special character.");
        }
    }
    
    
    if (errors.length > 0) {
        passwordError.textContent = errors.join("\n");
        isValid = false;
    } else {
        passwordError.textContent = "";
        isValid = true;
    }
    

    if (!isValid) {
        createFlashMessage(flashMessagesTypes.error, "Please add valid information");
    }
};
