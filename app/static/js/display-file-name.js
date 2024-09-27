function displayFileName() {
    const input = document.getElementById('upload-file-btn');
    const fileNameParagraph = document.getElementById('file-name');
    const fileName = input.value.length > 0 ? input.files[0].name : "No file chosen";
    fileNameParagraph.innerText = fileName;
    return fileName
  }