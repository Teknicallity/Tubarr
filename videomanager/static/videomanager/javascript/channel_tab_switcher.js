import {initializeCarousel} from "./channel.js";

const home_tab = document.querySelector("#home-tab")
const videos_tab = document.querySelector("#videos-tab")
const playlists_tab = document.querySelector("#playlists-tab")

const inner_content = document.querySelector("#inner-content")
const gridDisplayAmount = 40

home_tab.addEventListener("click", () => {
    console.log('homeclick')
    setActiveTab("#home-tab")
    history.pushState("", `${channelName} Home`, `/c=${channelId}`)
    inner_content.innerHTML = `<p>Loading</p>`;
    inner_content.innerHTML = `
    <p>Recent Videos:</p>
    <div id="video-carousel" class="carousel">
        <div class="carousel-viewport">
            <div class="carousel-track" id="video-carousel-inner"></div>
        </div>
        <button class="carousel-control-prev" id="prev-video-btn">Previous</button>
        <button class="carousel-control-next" id="next-video-btn">Next</button>
    </div>
    <p>Recent Playlists:</p>
    `;

    initializeCarousel()
})
videos_tab.addEventListener("click", () => {
    setActiveTab("#videos-tab")
    history.pushState("", `${channelName} Videos`, `/c=${channelId}/videos/`)
    inner_content.innerHTML = `<p>Loading</p>`
    let initialUrl = `/api/channels/${channelId}/videos/?page_size=${gridDisplayAmount}`

    fetchPage(initialUrl).then(videoList => {
        if (videoList.length === 0) {
            inner_content.innerHTML = `<p>No Videos</p>`
            return
        }

        let gridContent = ""
        videoList.forEach(video => {
            gridContent += `
            <article class="video-entry">
                <a href="/c=${video.channel.channel_id}/v=${video.video_id}/" class="entry-link">
                    <div class="entry-content">
                        <img class="thumbnail" src="${video.thumbnail}" alt="playlist thumbnail">
                        <p class="entry-title">${video.title}</p>
                        <div class="entry-metadata">
                            <img src="${video.channel.profile_image}" alt="pfp" class="avatar">
                            <div class="metadata-text">
                                <p href="youtube.com" class="entry-channel">${video.channel.name}</p>
                                <p class="entry-date">${video.upload_date}</p>
                            </div>
                        </div>
                    </div>
                </a>
            </article>
            `
        })
        inner_content.innerHTML = `
        <div class="content-grid">
            ${gridContent}
        </div>
        `

    })
})
playlists_tab.addEventListener("click", () => {
    setActiveTab("#playlists-tab")
    history.pushState("", `${channelName} Playlists`, `/c=${channelId}/playlists/`)
    inner_content.innerHTML = `<p>Loading</p>`
    let initialUrl = `/api/channels/${channelId}/playlists/?page_size=${gridDisplayAmount}`

    fetchPage(initialUrl).then(playlistList => {
        if (playlistList.length === 0) {
            inner_content.innerHTML = `<p>No Playlists</p>`
            return
        }

        let gridContent = ""
        playlistList.forEach(playlist => {
            gridContent += `
            <article class="video-entry">
                <a href="/c=${playlist.channel.channel_id}/p=${playlist.playlist_id}/" class="entry-link">
                    <div class="entry-content">
                        <img class="thumbnail" src="${playlist.thumbnail}" alt="playlist thumbnail">
                        <p class="entry-title">${playlist.name}</p>
                        <div class="entry-metadata">
                            <img src="${playlist.channel.profile_image}" alt="pfp" class="avatar">
                            <div class="metadata-text">
                                <p href="youtube.com" class="entry-channel">${playlist.channel.name}</p>
                            </div>
                        </div>
                    </div>
                </a>
            </article>
            `
        })
        inner_content.innerHTML = `
        <div class="content-grid">
            ${gridContent}
        </div>
        `
    })
})


// const firstPattern = /(?<=<)(\S*)(?=>; rel="first")/i;
// const prevPattern = /(?<=<)(\S*)(?=>; rel="prev")/i;
// const nextPattern = /(?<=<)(\S*)(?=>; rel="next")/i;
// const lastPattern = /(?<=<)(\S*)(?=>; rel="last")/i;


async function fetchPage(url) {
    try {
        const response = await fetch(url);
        const data = await response.json();

        const linkHeader = response.headers.get("Link");
        if (linkHeader) {
            const links = parseLinkHeader(linkHeader);
            console.log("Parsed links:", links);
        }

        return data
    } catch (error) {
        console.error("Error fetching page:", error);
        return null
    }
}

function parseLinkHeader(header) {
    const links = {};
    const parts = header.split(",");
    parts.forEach(part => {
        const section = part.split(";");
        if (section.length === 2) {
            const url = section[0].replace(/<(.*)>/, "$1").trim();
            const rel = section[1].replace(/rel="(.*)"/, "$1").trim();
            links[rel] = url;
        }
    });
    return links;
}

function setActiveTab(tabId) {
    const tabs = document.querySelectorAll(".tab")
    tabs.forEach(tab => tab.classList.remove('active'))
    const activeTab = document.querySelector(`${tabId}`)
    activeTab.classList.add("active")
}
setActiveTab(activeTabId)