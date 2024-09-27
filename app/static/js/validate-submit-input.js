let submitBtn = document.getElementById("submit-btn");
submitBtn.addEventListener('click', function (e) {
    e.preventDefault();
    const fileName = displayFileName();
    if (fileName === "No file chosen") {
        createFlashMessage(flashMessagesTypes.error, "please upload PDF file");
    }
    else {
        // Submit the form if a file is chosen
        const form = document.getElementById('file-upload-form');
        form.submit();
    }
})