
function initializeCarousel({
                                       containerId,
                                       prevButtonId,
                                       nextButtonId,
                                       apiEndpoint,
                                       renderItem
                                   }) {
    const carouselInner = document.getElementById(containerId);
    const prevButton = document.getElementById(prevButtonId);
    const nextButton = document.getElementById(nextButtonId);

    let carouselViewport = document.querySelector(`#${containerId}-viewport`);
    let carouselInnerWidth = carouselInner.getBoundingClientRect().width;
    let leftValue = 0;
    carouselInner.style.left = leftValue + "px";

    let displayAmount = 6

    let items = [];
    let currentItemIndex = 0;
    let pagesRemaining = true;
    const nextPattern = /(?<=<)(\S*)(?=>; rel="Next")/i;
    let nextPageUrl = apiEndpoint;

    async function fetchItems() {
        try {
            if (!nextPageUrl) return;
            const response = await fetch(nextPageUrl);
            if (!response.ok) throw new Error('Network error');
            const newItems = await response.json();
            items.push(...newItems);

            const linkHeader = response.headers.get('link');
            pagesRemaining = linkHeader && linkHeader.includes(`rel="next"`);
            nextPageUrl = pagesRemaining ? linkHeader.match(nextPattern)[0] : null;

            return newItems;
        } catch (error) {
            console.error('Error fetching items:', error);
            carouselInner.innerHTML = `<p class="error-message">Failed to load items. Please try again later.</p>`;
            return null;
        }
    }

    function renderCarousel(newItems) {
        const newHtml = newItems.map(renderItem).join('');
        carouselInner.innerHTML += newHtml;
    }

    function debounce(func, delay) {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => func(...args), delay);
        };
    }

    function updateButtons() {
        const disabledColor = 'darkgray';
        const enabledColor = 'black';

        // Disable "Next" if all videos are visible or no more videos to fetch
        if (currentItemIndex + displayAmount >= items.length-1 && nextPageUrl === null) {
            nextButton.style.color = disabledColor;
            nextButton.disabled = true;
        } else {
            nextButton.style.color = enabledColor;
            nextButton.disabled = false;
        }

        // Disable "Prev" if at the start of the carousel
        if (currentItemIndex <= 0) {
            prevButton.style.color = disabledColor;
            prevButton.disabled = true;
        } else {
            prevButton.style.color = enabledColor;
            prevButton.disabled = false;
        }
    }

    function computeNumberOfCardsFit() {
        const cardWidth = parseFloat(document.querySelector(".carousel-item").getBoundingClientRect().width);
        const gap = parseFloat(window.getComputedStyle(carouselInner).getPropertyValue("gap"));
        const carouselViewportWidth = parseInt(window.getComputedStyle(carouselViewport).getPropertyValue('width'));

        // console.log('compute NumberOfCardsFit', displayAmount)
        return Math.floor((carouselViewportWidth + gap) / (cardWidth + gap))
    }

    function getTotalMovementSize() {
        const cardWidth = parseFloat(document.querySelector(".carousel-item").getBoundingClientRect().width);
        const gap = parseFloat(window.getComputedStyle(carouselInner).getPropertyValue("gap"));

        return (cardWidth + gap) * displayAmount;
    }

    prevButton.addEventListener("click", () => {
        currentItemIndex = Math.max(0, currentItemIndex - displayAmount);
        leftValue += getTotalMovementSize()
        if (leftValue > 0) leftValue = 0;
        carouselInner.style.left = `${leftValue}px`;
        updateButtons();
    });

    nextButton.addEventListener("click", () => {
        currentItemIndex = Math.min(items.length - displayAmount, currentItemIndex + displayAmount);
        const carouselViewportWidth = carouselViewport.getBoundingClientRect().width;
        carouselInnerWidth = carouselInner.getBoundingClientRect().width;

        if (carouselInnerWidth - Math.abs(leftValue) > carouselViewportWidth) {
            leftValue -= getTotalMovementSize();
            carouselInner.style.left = `${leftValue}px`;
        }

        if (currentItemIndex + displayAmount >= items.length && nextPageUrl) {
            fetchItems().then(newItems => {
                if (newItems) {
                    renderCarousel(newItems);
                    updateButtons();
                    carouselInnerWidth = carouselInner.getBoundingClientRect().width;
                }
            });
        }
        updateButtons();
    });

    // Initial fetch
    fetchItems().then(newItems => {
        if (newItems) {
            renderCarousel(newItems);
            displayAmount = computeNumberOfCardsFit();
            updateButtons();
        }
    });

    window.addEventListener(
        "resize",
        debounce(() => {
            // Get the updated carousel width and card width
            const carouselInnerWidth = carouselInner.getBoundingClientRect().width;
            const cardWidth = parseFloat(document.querySelector(".carousel-item").getBoundingClientRect().width);
            const gap = parseFloat(window.getComputedStyle(carouselInner).getPropertyValue("gap"));

            displayAmount = computeNumberOfCardsFit();

            leftValue = -currentItemIndex * (cardWidth + gap);

            carouselInner.style.left = `${leftValue}px`;
        }, 200)
    );
}


const home_tab = document.querySelector("#home-tab")
const videos_tab = document.querySelector("#videos-tab")
const playlists_tab = document.querySelector("#playlists-tab")

const inner_content = document.querySelector("#inner-content")
const gridDisplayAmount = 40

home_tab.addEventListener("click", () => {
    console.log('homeclick')
    setActiveTab("#home-tab")
    // history.pushState("", `${channelName} Home`, `/c=${channelId}`)
    inner_content.innerHTML = `<p>Loading</p>`;
    inner_content.innerHTML = `
    <p>Recent Videos:</p>
    <div id="video-carousel" class="carousel">
        <div class="carousel-viewport" id="video-carousel-inner-viewport">
            <div class="carousel-track" id="video-carousel-inner"></div>
        </div>
        <div class="video-carousel-buttons">
            <button class="carousel-control" id="prev-video-btn"><</button>
            <button class="carousel-control" id="next-video-btn">></button>
        </div>
    </div>
    <p>Recent Playlists:</p>
    <div id="playlist-carousel" class="carousel">
        <div class="carousel-viewport" id="playlist-carousel-inner-viewport">
            <div class="carousel-track" id="playlist-carousel-inner"></div>
        </div>
        <div class="video-carousel-buttons">
            <button class="carousel-control" id="prev-playlist-btn"><</button>
            <button class="carousel-control" id="next-playlist-btn">></button>
        </div>
    </div>
    `;

    initializeCarousel({
        containerId: 'video-carousel-inner',
        prevButtonId: 'prev-video-btn',
        nextButtonId: 'next-video-btn',
        apiEndpoint: `/api/channels/${channelId}/videos/?page=1`,
        renderItem: video => `
        <article class="video-entry carousel-item">
            <a href="/c=${video.channel.channel_id}/v=${video.video_id}/" class="entry-link">
                <div class="entry-content">
                    <img class="thumbnail" src="${video.thumbnail}" alt="video thumbnail">
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
    });

    initializeCarousel({
        containerId: 'playlist-carousel-inner',
        prevButtonId: 'prev-playlist-btn',
        nextButtonId: 'next-playlist-btn',
        apiEndpoint: `/api/channels/${channelId}/playlists/?page=1`,
        renderItem: playlist => `
        <article class="video-entry carousel-item">
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
    });
})
videos_tab.addEventListener("click", () => {
    setActiveTab("#videos-tab")
    // history.pushState("", `${channelName} Videos`, `/c=${channelId}/videos/`)
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
    // history.pushState("", `${channelName} Playlists`, `/c=${channelId}/playlists/`)
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