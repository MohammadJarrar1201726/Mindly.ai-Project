function regenerateSummarizationContent(url) {
    const paragraphText = document.getElementById('modal-content').textContent;
    if (!paragraphText) {
        createFlashMessage(flashMessagesTypes.error, "no content to regenerate");
    } else {
        fetch(`${url}/regenerate-summarization-content`, {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ text: paragraphText }),
        }).then(response => {
            // Check if the response is successful
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }

            if(response.status == 422) {
                throw new Error("Text is so small and can't regenerate it " + response.statusText);
            }

            // Parse the JSON from the response
            return response.json();
        })
            .then(data => {
                // Display the summarized text in the HTML
                document.getElementById('modal-content').innerText = data.text;
            })
            .catch(error => {
                // Handle any errors
                console.error('There has been a problem with your fetch operation:', error);
                createFlashMessage(flashMessagesTypes.error, "Can't regenerate summarization now, try again later.")
            });
    }

}