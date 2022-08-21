function UpdateText() {
    var textArea = document.getElementById("textarea");
    var color = document.getElementById("font-color").value;
    var fontSize = document.getElementById("font-size").value;
    var fontFamily = document.getElementById("font-style").value;
    textArea.style.color = color;
    textArea.style.fontSize = fontSize + "px";
    textArea.style.fontFamily = fontFamily;
}

function save() {
    //save the textarea contents with its current font and color to a text file
    var textToWrite = document.getElementById("textarea").value;
    var textFileAsBlob = new Blob([textToWrite], {type:'text/plain'});
    var fileNameToSaveAs = "text.txt"
    var downloadLink = document.createElement("a");
    downloadLink.download = fileNameToSaveAs;
    downloadLink.innerHTML = "Download File";
    if (window.webkitURL != null) {
        // Chrome allows the link to be clicked
        // without actually adding it to the DOM.
        downloadLink.href = window.webkitURL.createObjectURL(textFileAsBlob);
    }
    else {
        // Firefox requires the link to be added to the DOM
        // before it can be clicked.
        downloadLink.href = window.URL.createObjectURL(textFileAsBlob);
        downloadLink.onclick = destroyClickedElement;
        downloadLink.style.display = "none";
        document.body.appendChild(downloadLink);
    }
    downloadLink.click();
}
 