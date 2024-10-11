const carouselInner = document.getElementById('carousel-inner');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');

let videos = [];
let currentIndex = 0;
let pagesRemaining = true;
const displayAmount = 4;
const nextPattern = /(?<=<)(\S*)(?=>; rel="Next")/i;
let nextPageUrl = "/api/videos/?page=1"

async function fetchVideos() {
    if (nextPageUrl === "") {
        return
    }
    const response = await fetch(`${nextPageUrl}`);
    let nextVideos = await response.json();
    videos.push(...nextVideos);

    const linkHeader = response.headers.get('link');
    pagesRemaining = linkHeader && linkHeader.includes(`rel=\"next\"`);

    if (pagesRemaining) {
        nextPageUrl = linkHeader.match(nextPattern)[0];
    } else {
        nextPageUrl = ""
    }
}

function renderCarousel() {
    let maxEntryIndex = Math.min(currentIndex + displayAmount, videos.length);
    carouselInner.innerHTML = videos.slice(currentIndex, maxEntryIndex).map(video => `
        <div class="video-entry">
                <a href="/c=${video.channel.channel_id}/v=${video.video_id}/" class="entry-link">
                    <div class="thumbnail-container">
                        <img class="thumbnail" src="${video.thumbnail}" alt="video thumbnail">
                    </div>
                    <div class="entry-text">
                        <p class="entry-title">${video.title}</p>
                        <div class="entry-metadata">
                            <div class="channel-avatar">
                                <img src="${video.channel.profile_image}" alt="pfp" class="avatar">
                            </div>
                            <div class="metadata-text">
                                <p href="youtube.com" class="entry-channel">${video.channel.name}</p>
                                <p class="entry-date">${video.upload_date}</p>
                            </div>
                        </div>
                    </div>
                </a>
            </div>
    `).join('');
}

function updateButtons(){
    const disabledColor = 'darkgray'
    const enabledColor = 'black'
    if (currentIndex + displayAmount >= videos.length) {
        nextBtn.style.color = disabledColor;
    } else {
        nextBtn.style.color = enabledColor;
    }

    if (currentIndex - displayAmount < 0) {
        prevBtn.style.color = disabledColor;
    } else {
        prevBtn.style.color = enabledColor;
    }
}

function updateCarousel() {
    const items = document.querySelectorAll('.carousel-item');
    items.forEach((item, index) => {
        item.style.transform = `translateX(${(index - currentIndex) * 100}%)`;
    });
}

prevBtn.addEventListener('click', () => {
    currentIndex = (currentIndex - displayAmount >= 0) ? currentIndex - displayAmount : currentIndex;
    renderCarousel();
    updateButtons();
});

nextBtn.addEventListener('click', () => {
    currentIndex = (currentIndex + displayAmount < videos.length) ? currentIndex + displayAmount : currentIndex;

    if (currentIndex + displayAmount >= videos.length) {
        fetchVideos().then(() => {
            renderCarousel();
            updateButtons();
        })
    } else {
        renderCarousel();
        updateButtons();
    }
});

// Initial fetch
fetchVideos().then(() => {
    renderCarousel();
    updateButtons()
})