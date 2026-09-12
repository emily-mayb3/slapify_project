var currentAudioId = null;
let queue = []; // queue will just hold ids of songs

// source = 0 -> single song, source = 1 -> queue
function playAudio(source = 0, id) {
    // destroy previous song being played if playing single song
    if (currentAudioId != id && source == 0) {
        if (currentAudioId != null) {
            document.getElementById(currentAudioId).pause();
            document.getElementById(currentAudioId).currentTime = 0;
            clearQueue();
        }
        queue.push(id);
    }

    // play next song in queue
    var audio = document.getElementById(queue[0]);
    var progressBar = document.getElementById('progress-bar')
    currentAudioId = queue[0];

    if (audio.paused) {
        audio.play();
        updateProgressBar(audio, progressBar)
    } else {
        audio.pause();
    }
}

function updateProgressBar(audio, progressBar) {
    var progress = (audio.currentTime / audio.duration * 100);
    progressBar.value = progress;
    if (progress == 100) {
        clearTimeout(this.timeoutId);
        progress = 0;
        removeSongFromQueue(queue[0]);
        if (queue.length > 0) {
            playAudio(1, queue[0]);
        } else {
            currentAudioId = null;
        }
    }

    if (!audio.paused && progress < 100) {
        this.timeoutId = setTimeout(function () {
            updateProgressBar(audio, progressBar);
        }, 100);
    }
}

// Add event listener to the progress bar for seeking
function seekAudio(e) {
    var audio = document.getElementById(currentAudioId);
    var progressBar = e.target;
    var pos = (e.offsetX / progressBar.offsetWidth) * audio.duration;

    // Ensure audio is loaded
    if (audio.readyState >= 2) {
        audio.currentTime = pos;
    } else {
        audio.addEventListener('loadeddata', function () {
            audio.currentTime = pos;
        });
    }
}

function addSongToQueue(id) {
    // Add the song to the queue if it's not already in it
    if (!queue.includes(id)) {
        queue.push(id);
    }
    // play song if no song is currently playing
    if (currentAudioId == null) {
        playAudio(1, id);
    }
}

function removeSongFromQueue(id) {
    // Remove the song from the queue if it's in it
    if (queue.includes(id)) {
        var index = queue.indexOf(id);
        queue.splice(index, 1);
    }
}

function clearQueue() {
    queue = [];
}
