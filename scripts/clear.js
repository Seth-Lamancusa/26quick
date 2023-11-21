document.getElementById('clearLocalStorage').addEventListener('click', function () {
    // Clear local storage
    localStorage.clear();
    updateSessionPlot();
    alert('Local storage cleared!');
});