function updateSessionPlot() {

    let rawData = {};
    for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        rawData[key] = localStorage.getItem(key);
    }

    const sortedKeys = Object.keys(rawData).sort();
    let runs = 0;

    sortedKeys.forEach((key) => {
        const value = rawData[key];
        if (value === 'end') {
            runs += 1;
        }
    });


    document.getElementById('runsCount').innerHTML = `
        Runs in Local Storage: ${runs}
    `;

}

updateSessionPlot();






