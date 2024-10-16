document.addEventListener('DOMContentLoaded', function() {
    // Toggle play/pause button
    const playButton = document.querySelector('.fa-play');
    playButton.addEventListener('click', function() {
        this.classList.toggle('fa-play');
        this.classList.toggle('fa-pause');
    });

    // Toggle karaoke mode
    const karaokeButton = document.querySelector('.fa-microphone');
    karaokeButton.addEventListener('click', function() {
        this.classList.toggle('text-primary');
    });

    // Simulate progress bar movement
    const progressBar = document.querySelector('.progress-bar');
    let progress = 0;
    setInterval(() => {
        progress = (progress + 1) % 101;
        progressBar.style.width = `${progress}%`;
    }, 1000);
});

<Fab color="primary">
  <img src="logo.png" alt="Custom icon" />
</Fab>