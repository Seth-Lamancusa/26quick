document.getElementById('downloadLocalStorage').addEventListener('click', function () {
    // Convert localStorage to string
    const dataStr = JSON.stringify(localStorage, null, 4); // The third parameter "4" is for pretty print with 4 spaces

    // Create a Blob from the data
    const blob = new Blob([dataStr], { type: 'application/json' });

    // Create a download link using the Blob URL
    const url = window.URL.createObjectURL(blob);
    const downloadLink = document.createElement('a');

    // Get current datetime and format it as "YYYY-MM-DD_HH-MM-SS"
    const now = new Date();
    const formattedDatetime = now.toISOString().slice(0, 19).replace(/:/g, '-').replace('T', '_');

    downloadLink.href = url;
    downloadLink.download = `localStorage_${formattedDatetime}.json`;

    // Append the link to the document and trigger the download
    document.body.appendChild(downloadLink);
    downloadLink.click();

    // Clean up
    document.body.removeChild(downloadLink);
    window.URL.revokeObjectURL(url);
});

