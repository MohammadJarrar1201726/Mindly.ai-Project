const handleFormSubmit = async (formElement, url, isSignUp = false) => {
    try {
        formElement.addEventListener('submit', async function (event) {
            event.preventDefault();

            const formData = new FormData(this);
            const data = new URLSearchParams([...formData]);


            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: data.toString(),
            });


            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Error: ${errorText || response.statusText}`);
            }

            const result = await response.json();

            if (isSignUp && response.ok) {
                createFlashMessage(flashMessagesTypes.success, 'Account created successfully! Please sign in to continue.');
                setTimeout(() => {
                    window.location.href = '/signin';
                }, 2000);
            } else if (result.login) {
                createFlashMessage(flashMessagesTypes.success, 'You have successfully logged in! Redirecting...');
                setTimeout(() => {
                    window.location.href = '/mindMap';
                }, 1500);
            } else {
                createFlashMessage(flashMessagesTypes.error,  'Login failed. Please try again.');
            }
        });
    } catch (error) {
        createFlashMessage(flashMessagesTypes.error, 'An unexpected error occurred. Please try again.');
    }
};

// Handle the sign-in and sign-up form submissions
document.addEventListener('DOMContentLoaded', () => {
    const signInForm = document.getElementById('sign-in-form');
    const signUpForm = document.getElementById('sign-up-form');

    if (signInForm) {
        handleFormSubmit(signInForm, '/signin');
    }
    if (signUpForm) {
        handleFormSubmit(signUpForm, '/signup', true);
    }
});
