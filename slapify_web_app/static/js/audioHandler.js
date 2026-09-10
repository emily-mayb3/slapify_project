var currentAudioId = null;

function playAudio(id) {
    // destroy previous song being played
    if (currentAudioId != null && currentAudioId != id) {
        document.getElementById(currentAudioId).pause();
        document.getElementById(currentAudioId).currentTime = 0;
    }

    var audio = document.getElementById(id);
    var progressBar = document.getElementById('progress-bar')
    currentAudioId = id;

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

    if (!audio.paused && progress < 100) {
        setTimeout(function () {
            updateProgressBar(audio, progressBar);
        }, 1000);
    }
}

// Add event listener to the progress bar for seeking
function seekAudio(e) {
    var audio = document.getElementById(currentAudioId);
    console.log('Audio:', audio);
    var progressBar = e.target;
    console.log('ProgressBar:', progressBar);
    var pos = (e.offsetX / progressBar.offsetWidth) * audio.duration;
    console.log('Position:', pos);

    // Ensure audio is loaded
    if (audio.readyState >= 2) {
        audio.currentTime = pos;
    } else {
        audio.addEventListener('loadeddata', function () {
            audio.currentTime = pos;
        });
    }
}