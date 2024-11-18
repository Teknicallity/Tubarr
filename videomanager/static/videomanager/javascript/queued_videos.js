queuedVideosDiv = document.getElementById("queued-videos");
erroredVideosDiv = document.getElementById("errored-videos");
noContentDiv = document.getElementById("no-queued");

let lastQueuedCount = 0;
let lastErroredCount = 0;

function updateQueuedVideos() {
    const updateUrl = document.getElementById("updateUrl").innerText;
    console.log(updateUrl)
    fetch(updateUrl).then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    }).then(data => {
        if (data.queued_videos && data.queued_videos.length !== lastQueuedCount) {
            lastQueuedCount = data.queued_videos.length;
            if (data.queued_videos.length > 0) {
                let queuedColumnContent = "<h2 class=\"column-title\">Queued</h2>"

                data.queued_videos.forEach(video => {
                    queuedColumnContent += `
                        <article class="horizontal-video-entry">
                            <a href="/c=${video.channel.channel_id}/v=${video.video_id}/" class="entry-link">
                                <div class="video-entry-content">
                                    <img src="${video.thumbnail}" alt="thumbnail" class="thumbnail">
                                    <div class="entry-text">
                                        <p class="horizontal-title">${video.title}</p>
                                        <div class="horizontal-metadata">
                                            <img src="${video.channel.profile_image}" alt="pfp"
                                                 class="horizontal-avatar">
                                            <div class="metadata-text">
                                                <p href="youtube.com"
                                                   class="horizontal-channel">${video.channel.name}</p>
                                                <p class="horizontal-date">${video.upload_date}</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </a>
                        </article>
                    `
                })
                queuedVideosDiv.innerHTML = queuedColumnContent
                queuedVideosDiv.style.display = 'grid';
                noContentDiv.innerHTML = ''
            } else {
                queuedVideosDiv.innerHTML = ``
                queuedVideosDiv.style.display = 'none';
            }
        }

        if (data.errored_videos && data.errored_videos.length !== lastErroredCount) {
            lastErroredCount = data.errored_videos.length;
            if (data.errored_videos && data.errored_videos.length > 0) {
                let erroredColumnContent = "<h2 class=\"column-title\">Errored</h2>"

                data.errored_videos.forEach(video => {
                    erroredColumnContent += `
                    <article class="horizontal-video-entry">
                        <a href="/c=${video.channel.channel_id}/v=${video.video_id}/" class="entry-link">
                            <div class="video-entry-content">
                                <img src="${video.thumbnail}" alt="thumbnail" class="thumbnail">
                                <div class="entry-text">
                                    <p class="horizontal-title">${video.title}</p>
                                    <div class="horizontal-metadata">
                                        <img src="${video.channel.profile_image}" alt="pfp"
                                             class="horizontal-avatar">
                                        <div class="metadata-text">
                                            <p href="youtube.com"
                                               class="horizontal-channel">${video.channel.name}</p>
                                            <p class="horizontal-date">${video.upload_date}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </a>
                    </article>
                `
                })
                erroredVideosDiv.innerHTML = erroredColumnContent
                erroredVideosDiv.style.display = 'grid';
                noContentDiv.innerHTML = ''
            } else {
                erroredVideosDiv.innerHTML = ``
                erroredVideosDiv.style.display = 'none';
            }
        }

        if (lastQueuedCount + lastErroredCount > 0) {
            noContentDiv.innerHTML = ''
        } else {
            noContentDiv.innerHTML = 'No Queued Downloads'
        }
    })
}

setInterval(updateQueuedVideos, 2000);