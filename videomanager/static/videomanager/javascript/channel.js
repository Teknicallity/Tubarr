const carouselInner = document.getElementById('carousel-inner');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');

let videos = [];
let currentIndex = 0;
let nextPage = 1;
let pagesRemaining = true;
const displayAmount = 4;
const nextPattern = /(?<=<)(\S*)(?=>; rel="Next")/i;
let url = "/api/videos/?page=1"

async function fetchVideos() {
    if (url === "") {
        return
    }
    const response = await fetch(`${url}`); // Adjust the API endpoint as needed
    // nextPage++;
    let nextVideos = await response.json();
    console.log(nextVideos)
    videos.push(...nextVideos);

    const linkHeader = response.headers.get('link');
    console.log(linkHeader)
    pagesRemaining = linkHeader && linkHeader.includes(`rel=\"next\"`);

    if (pagesRemaining) {
        url = linkHeader.match(nextPattern)[0];
    } else {
        url = ""
    }
    console.log(`url '${url}'`)
    console.log(videos)
    // renderCarousel();
}

function renderCarousel() {
    // <div class="carousel-item">
    //     <img src="${video.thumbnail}" alt="${video.title}">
    //     <h3 class="item-title">${video.title}</h3>
    //     <p>Uploaded on: ${video.upload_date}</p>
    // </div>
    let maxEntryIndex = Math.min(currentIndex + displayAmount, videos.length);
    console.log("maxEntry index", maxEntryIndex);
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
    // updateCarousel();
}

function updateCarousel() {
    const items = document.querySelectorAll('.carousel-item');
    items.forEach((item, index) => {
        item.style.transform = `translateX(${(index - currentIndex) * 100}%)`;
    });
}

prevBtn.addEventListener('click', () => {
    console.log("currentIndex", currentIndex);
    currentIndex = (currentIndex - displayAmount >= 0) ? currentIndex - displayAmount : currentIndex;
    console.log("updated currentIndex", currentIndex);
    renderCarousel();
});

nextBtn.addEventListener('click', () => {
    console.log("currentIndex", currentIndex);
    currentIndex = (currentIndex + displayAmount < videos.length) ? currentIndex + displayAmount : currentIndex;
    console.log("updated currentIndex", currentIndex);
    // updateCarousel();

    if (currentIndex + displayAmount >= videos.length) {
        fetchVideos().then(() => {
            renderCarousel();
        })
    } else {
        renderCarousel();
    }
});

// Initial fetch
fetchVideos().then(() => {
    renderCarousel();
})
// render
// on next button click,
//     change window
//     check if end+windowsize is out of range
//         fetchvideos