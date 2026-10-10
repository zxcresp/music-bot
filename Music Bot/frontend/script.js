const tg = window.Telegram.WebApp;

tg.ready();

async function loadSongs() {
    console.log("NEW SCRIPT LOADED");
    const songsContainer = document.getElementById("songs");

    try {
        songsContainer.textContent = "Loading...";
        const response = await fetch("/songs", {
            method: "POST",
            headers: {"Content-Type": "application/json"},body: JSON.stringify({init_data: tg.initData})});
        console.log("Songs response:", response.status);

        if (!response.ok) {
            throw new Error(`Failed to load songs: ${response.status}`);
        }
        const songs = await response.json();

        songsContainer.innerHTML = "";

        if (songs.length === 0) {
            songsContainer.textContent = "Your music library is empty.";
            return;
        }

        songs.forEach(song => {
            const songElement = document.createElement("div");
            songElement.className = "song";

            const songInfo = document.createElement("div");
            songInfo.className = "song-info";

            const songTitle = document.createElement("div");
            songTitle.className = "song-title";
            songTitle.textContent = song.title;

            const songDuration = document.createElement("div");
            songDuration.className = "song-duration";
            songDuration.textContent = formatDuration(song.duration);

            const playButton = document.createElement("button");
            playButton.className = "play-button";
            playButton.textContent = "▶";
            playButton.type = "button";

            songInfo.appendChild(songTitle);
            songInfo.appendChild(songDuration);

            songElement.appendChild(songInfo);
            songElement.appendChild(playButton);

            songsContainer.appendChild(songElement);

            playButton.addEventListener("click", async () => {
                console.log("PLAY BUTTON CLICKED", song.id, song.title);
                const player = document.getElementById("audio-player");

                if (!player) {
                    console.error('Element with id "audio-player" not found.');
                    alert("Audio player is missing from index.html.");
                    return;
                }

                try {
                    playButton.disabled = true;
                    console.log("Requesting song:", song.id, song.title);

                    const audioResponse = await fetch("/audio", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            init_data: tg.initData,
                            song_id: song.id
                        })
                    });

                    console.log("Audio response:", audioResponse.status);

                    if (!audioResponse.ok) {
                        const errorText = await audioResponse.text();
                        throw new Error(
                            `Audio request failed (${audioResponse.status}): ${errorText}`
                        );
                    }

                    const audioBlob = await audioResponse.blob();
                    console.log("Audio signature:", new Uint8Array(
                        await audioBlob.slice(0, 16).arrayBuffer()
                    ));
                    console.log("Player element:", player);
                    console.log("Audio error:", player.error);
                    console.log("Audio size:", audioBlob.size);
                    console.log("Audio type:", audioBlob.type);

                    if (audioBlob.size === 0) {
                        throw new Error("The received audio file is empty.");
                    }

                    if (player.dataset.objectUrl) {
                        URL.revokeObjectURL(player.dataset.objectUrl);
                    }

                    const audioUrl = URL.createObjectURL(audioBlob);

                    player.dataset.objectUrl = audioUrl;
                    player.src = audioUrl;
                    player.load();

                    await player.play();

                    console.log("Playback started:", song.title);

                } catch (error) {
                    console.error("Playback error:", error);
                    alert(`Could not play song: ${error.message}`);
                } finally {
                    playButton.disabled = false;
                }
            });
        });

    } catch (error) {
        console.error("Failed to load songs:", error);
        songsContainer.textContent = `Error: ${error.message}`;
    }
}

function formatDuration(seconds) {
    if (typeof seconds !== "number" || !Number.isFinite(seconds)) {
        return "0:00";
    }

    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;

    return `${minutes}:${remainingSeconds.toString().padStart(2, "0")}`;
}

loadSongs();
