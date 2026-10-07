//console.log("SCRIPT STARTED");
const tg = window.Telegram.WebApp;

tg.ready();

async function loadSongs() {
    const songsContainer = document.getElementById("songs");

    try {
        songsContainer.textContent = "Loading...";
        //console.log("Starting loadSongs");
        //console.log("initData:", tg.initData);
        const response = await fetch("/songs", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                init_data: tg.initData
            })
        });

        //console.log("Response status:", response.status);

        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }

        const songs = await response.json();

        songsContainer.innerHTML = "";

        songs.forEach(song => {
            const songElement = document.createElement("div");

            songElement.className = "song";

            songElement.innerHTML = `
                <div class="song-info">
                    <div class="song-title">${song.title}</div>
                    <div class="song-duration">
                        ${formatDuration(song.duration)}
                    </div>
                </div>

                <button class="play-button">
                    ▶
                </button>
            `;

            songsContainer.appendChild(songElement);
        });

    } catch (error) {
        console.error(error);
        songsContainer.textContent = `Error: ${error.message}`;
    }
}


function formatDuration(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;

    return `${minutes}:${remainingSeconds.toString().padStart(2, "0")}`;
}

loadSongs();