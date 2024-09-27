// Function to export the diagram as an image
function exportMindmap(diagramId, buttonId) {
    document.getElementById(buttonId).addEventListener("click", function(event) {
        event.preventDefault();
        var myDiagram = go.Diagram.fromDiv(diagramId);
        // Generate the image data based on the diagram's current size
        var imgData = myDiagram.makeImageData({
            background: "white",       // Set the background color
            returnType: "image/png",   // Specify the image format
            scale: 1,                  // Use scale of 1 to export at actual size
        });
        
        var link = document.createElement("a");
        link.href = imgData;
        link.download = "mindmap.png"; // Set the file name
        
        link.click();
    });
}

