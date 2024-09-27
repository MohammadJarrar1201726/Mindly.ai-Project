let isGenerating = false; // To prevent double-click

document.getElementById("icon-download-pdf").addEventListener("click", function() {
    if (isGenerating) return;  // Prevent double-clicks

    isGenerating = true;  // Set flag to prevent further clicks
    const icon = document.getElementById("icon-download-pdf");
    const spinner = document.getElementById("spinner");

    // Hide the icon and show the spinner
    icon.style.display = 'none';
    spinner.style.display = 'block';

    fetch('/generate_pdf', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => {
        if (response.ok) {
            return response.json();  // Expecting JSON response with the filename
        } 
        else{
            if(response.status === 500){
                throw new Error('Error in generating pdf');
            }
            else if(response.status === 404){
                throw new Error('File not found');
            }
            else{
                throw new Error('An error occur while generating pdf');
            }
        }


        
    })
    .then(data => {
     
            const filename = data.filename;  // Get filename from the response
            
            
            // Create an anchor element to download the file
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = downloadUrl;
            a.download = filename;
            document.body.appendChild(a);
            a.click();  // Trigger download
            // Hide the spinner and show the icon
            spinner.style.display = 'none';
            icon.style.display = 'block';
            document.body.removeChild(a);  // Clean up
       
    })
    .catch(error => {
        createFlashMessage(flashMessagesTypes.error, error.message);
        spinner.style.display = 'none';
        icon.style.display = 'block';
    })
    
    .finally(() => {
        isGenerating = false;  // Allow clicks again
    });
});
