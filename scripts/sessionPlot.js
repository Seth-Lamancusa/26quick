var ctx = document.getElementById('session_plot').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        datasets: [{
            label: 'Time',
            backgroundColor: '#a070a0',
            borderColor: '#a070a0',
            yAxisID: 'y-axis-time',
            data: []
        }, {
            label: 'Mistakes',
            backgroundColor: '#3a1862',
            borderColor: '#3a1862',
            yAxisID: 'y-axis-mistakes',
            data: []
        }]
    },
    options: {
        maintainAspectRatio: true,
        aspectRatio: 1,
        plugins: {
            legend: {
                display: true,
                position: 'bottom',
            },
        },
        scales: {
            x: {
                display: false // Hide x-axis labels
            },
            'y-axis-time': {
                type: 'linear',
                position: 'left',
            },
            'y-axis-mistakes': {
                type: 'linear',
                position: 'right',
                grid: {
                    drawOnChartArea: false
                }
            }
        },
        layout: {
            padding: {
                left: 20,
                right: 20,
                top: 40,
                bottom: 10
            }
        },
    }
});

function updateSessionPlot() {
    myChart.data.datasets[0].data = [];
    myChart.data.datasets[1].data = [];
    myChart.data.labels = [];

    let rawData = {};
    for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        rawData[key] = localStorage.getItem(key);
    }

    const sortedKeys = Object.keys(rawData).sort();
    let runs = [];
    let currentRun = null;
    let runIndex = 1; // Initialize counter for x values

    // Variables for calculations
    let totalMistakes = 0;
    let totalTime = 0;
    let bestTime = Number.POSITIVE_INFINITY;
    let bestMistakes = Number.POSITIVE_INFINITY;
    let worstTime = Number.NEGATIVE_INFINITY;
    let worstMistakes = Number.NEGATIVE_INFINITY;

    sortedKeys.forEach((key) => {
        const value = rawData[key];
        console.log(key, value);
        if (value === 'start') {
            currentRun = { startTime: key, mistakes: 0 };
        } else if (value === 'end') {
            if (currentRun) {
                currentRun.endTime = key;
                const runDuration = new Date(key) - new Date(currentRun.startTime);
                currentRun.duration = runDuration;
                runs.push(currentRun);

                // Update calculations
                totalMistakes += currentRun.mistakes;
                totalTime += runDuration;
                bestTime = Math.min(bestTime, runDuration);
                bestMistakes = Math.min(bestMistakes, currentRun.mistakes);
                worstTime = Math.max(worstTime, runDuration);
                worstMistakes = Math.max(worstMistakes, currentRun.mistakes);

                currentRun = null;
                myChart.data.labels.push('');
            }
        } else {
            const parts = value.split(',');
            if (parts.length === 5) {
                currentRun.mistakes = Math.max(currentRun.mistakes, parseInt(parts[4], 10));
            }
        }
    });

    const runData = runs.map(run => {
        return {
            x: runIndex++, // Use the runIndex as the x value and increment it for each run
            yTime: run.duration,
            yMistakes: run.mistakes
        };
    });

    // Add new data
    myChart.data.datasets[0].data = runData.map(run => ({ x: run.x, y: run.yTime }));
    myChart.data.datasets[1].data = runData.map(run => ({ x: run.x, y: run.yMistakes }));

    // Update HTML with calculations
    const averageTime = totalTime / runs.length;
    const averageMistakes = totalMistakes / runs.length;
    document.getElementById('stats').innerHTML = `
        Average Time: ${Math.round(averageTime)} ms<br>
        Average Mistakes: ${Math.round(averageMistakes)}<br>
        Best Time: ${Math.round(bestTime)} ms<br>
        Best Mistakes: ${Math.round(bestMistakes)}<br>
        Worst Time: ${Math.round(worstTime)} ms<br>
        Worst Mistakes: ${Math.round(worstMistakes)} <br>
        Total Runs: ${runs.length} <br>
    `;

    myChart.update();
}




updateSessionPlot();






