var seconds = 0, minutes = 0, hours = 0;
var time;

function add() {
    seconds++;
    if (seconds >= 60) {
        seconds = 0;
        minutes++;
        if (minutes >= 60) {
            minutes = 0;
            hours++;
        }
    }
    
    document.getElementById('display').textContent = (hours ? (hours > 9 ? hours : "0" + hours) : "00") + ":" + (minutes ? (minutes > 9 ? minutes : "0" + minutes) : "00") + ":" + (seconds > 9 ? seconds : "0" + seconds);

    timer();
}
function timer() {
    time = setTimeout(add, 1000);
}

document.getElementById('start').onclick = function() {
    timer();
    document.getElementById('start').disabled = true;
    document.getElementById('stop').disabled = false;
    document.getElementById('reset').disabled = false;
    console.log("start")
}

document.getElementById('stop').onclick = function() {
    clearTimeout(time);
    document.getElementById('start').disabled = false;
    document.getElementById('stop').disabled = true;
}

document.getElementById('reset').onclick = function() {
    document.getElementById('display').textContent = "00:00:00";
    seconds = 0; minutes = 0; hours = 0;
    clearTimeout(time);
    document.getElementById('start').disabled = false;
    document.getElementById('stop').disabled = true;
    document.getElementById('reset').disabled = true;
}