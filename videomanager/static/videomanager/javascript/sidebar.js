
queuedDiv = document.getElementById("queued-div");
erroredDiv = document.getElementById("errored-div");

function fetchData() {
    const countUrl = document.getElementById("queued-url").innerText;

    fetch(countUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.queued_videos_count && data.queued_videos_count > 0) {
                queuedDiv.textContent = `Queued: ${data.queued}`;
            } else {
                queuedDiv.textContent = '';
            }

            if (data.errored_videos_count && data.errored_videos_count > 0) {
                erroredDiv.textContent = `Errored: ${data.errored}`;
            } else {
                erroredDiv.textContent = '';
            }
        })
        .catch(error => {
            console.error("Error fetching data:", error);
        });
}

setInterval(fetchData, 2000);