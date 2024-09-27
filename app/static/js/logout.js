// Function to handle logout
const handleLogout = async () => {
    try {
        const response = await fetch('/logout', {
            method: 'POST',
            credentials: 'include'  // Ensure cookies are sent with the request
        });

        if (response.ok) {
            // Display success flash message using the provided file
            createFlashMessage(flashMessagesTypes.success, 'You have been logged out successfully!');

            // Delay the redirection to allow the flash message to be visible
            setTimeout(() => {
                window.location.href = '/'; // Redirect to the home page
            }, 1000); // Adjust the delay to 3 seconds
        } else {
            // Display error flash message
            createFlashMessage(flashMessagesTypes.error, 'Logout failed. Please try again.');
        }
    } catch (error) {
        // Display error flash message
        createFlashMessage(flashMessagesTypes.error, 'An unexpected error occurred during logout.');
    }
};

window.onload=function(){
    document.getElementById('logout-icon').addEventListener('click', () => {
        handleLogout();
    });
    }