const carouselInner = document.getElementById('video-carousel-inner');
const prevBtn = document.getElementById('prev-video-btn');
const nextBtn = document.getElementById('next-video-btn');

let carouselVp = document.querySelector(".carousel-viewport");
let cCarouselInner = document.querySelector(".carousel-track");
let carouselInnerWidth = cCarouselInner.getBoundingClientRect().width;
let carouselItem = document.querySelector(".carousel-item");
let leftValue = 0;

let videos = [];
let currentIndex = 0;
let pagesRemaining = true;
const displayAmount = 6;
const nextPattern = /(?<=<)(\S*)(?=>; rel="Next")/i;
let nextPageUrl = "/api/videos/?page=1"

async function fetchVideos() {
    try {
        if (nextPageUrl === "") {
            return
        }
        const response = await fetch(`${nextPageUrl}`);
        if (!response.ok) throw new Error('Network error');
        let nextVideos = await response.json();
        videos.push(...nextVideos);

        const linkHeader = response.headers.get('link');
        pagesRemaining = linkHeader && linkHeader.includes(`rel=\"next\"`);

        if (pagesRemaining) {
            nextPageUrl = linkHeader.match(nextPattern)[0];
        } else {
            nextPageUrl = ""
        }
        return nextVideos;
    } catch (error) {
        console.error('Error fetching videos:', error);
        carouselInner.innerHTML = `<p class="error-message">Failed to load videos. Please try again later.</p>`;
        return null
    }
}

function renderCarousel(newVideos) {
    let newVidHtml = newVideos.map(video => `
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
    `).join('');

    if (carouselInner.innerHTML !== '') {
        carouselInner.innerHTML = carouselInner.innerHTML + newVidHtml
    } else {
        carouselInner.innerHTML = newVidHtml
    }
}

function debounce(func, delay) {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => func(...args), delay);
    };
}

function updateButtons() {
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

function showLoading() {
    carouselInner.innerHTML = `<div class="spinner">Loading...</div>`;
}

let windowWidth = window.innerWidth;
window.addEventListener('resize', debounce(() => {
    window.addEventListener('resize', function () {
        if (window.innerWidth !== windowWidth) {
            console.log(windowWidth)
        }
    });
}, 300))

// Initial fetch
// showLoading();
fetchVideos().then(newVideos => {
    renderCarousel(newVideos);
    updateButtons()
    carouselInnerWidth = cCarouselInner.getBoundingClientRect().width;
})

function getTotalMovementSize() {
    let cardWidth = parseFloat(document.querySelector(".carousel-item").getBoundingClientRect().width)
    let gap = parseFloat(window.getComputedStyle(cCarouselInner).getPropertyValue("gap"))
    let carouselVpWidth = parseInt(window.getComputedStyle(carouselVp).getPropertyValue('width'))
    let numberCardsInView = Math.floor(carouselVpWidth / cardWidth)
    return (cardWidth + gap) * numberCardsInView
}

prevBtn.addEventListener("click", () => {
    currentIndex = (currentIndex - displayAmount >= 0) ? currentIndex - displayAmount : currentIndex;
    if (!leftValue == 0) {
        leftValue -= -getTotalMovementSize();
        cCarouselInner.style.left = leftValue + "px";
    }
    updateButtons()
});

nextBtn.addEventListener("click", () => {
    currentIndex = (currentIndex + displayAmount < videos.length) ? currentIndex + displayAmount : currentIndex;
    const carouselVpWidth = carouselVp.getBoundingClientRect().width;
    if (carouselInnerWidth - Math.abs(leftValue) > carouselVpWidth) {
        leftValue -= getTotalMovementSize();
        cCarouselInner.style.left = leftValue + "px";
    }
    if (currentIndex + displayAmount >= videos.length) {
        // showLoading();
        fetchVideos().then(newVideos => {
            if (newVideos) {
                renderCarousel(newVideos);
                updateButtons();
                carouselInnerWidth = cCarouselInner.getBoundingClientRect().width;
            }
        })
    } else {
        updateButtons();
    }
});

const mediaQuery980 = window.matchMedia("(max-width: 980px)");
const mediaQuery1100 = window.matchMedia("(max-width: 1100px)");
const mediaQuery1330 = window.matchMedia("(max-width: 1330px)");
const mediaQuery1600 = window.matchMedia("(max-width: 1600px)");
const mediaQuery1900 = window.matchMedia("(max-width: 1900px)");
const mediaQuery2200 = window.matchMedia("(max-width: 2200px)");

mediaQuery980.addEventListener("change", mediaManagement);
mediaQuery1100.addEventListener("change", mediaManagement);
mediaQuery1330.addEventListener("change", mediaManagement);
mediaQuery1600.addEventListener("change", mediaManagement);
mediaQuery1900.addEventListener("change", mediaManagement);
mediaQuery2200.addEventListener("change", mediaManagement);

let oldViewportWidth = window.innerWidth;

function mediaManagement() {
    const totalMovementSize = getTotalMovementSize();
    const newViewportWidth = window.innerWidth;

    if (leftValue <= -totalMovementSize && oldViewportWidth < newViewportWidth) {
        leftValue += totalMovementSize;
        cCarouselInner.style.left = leftValue + "px";
        oldViewportWidth = newViewportWidth;
    } else if (
        leftValue <= -totalMovementSize &&
        oldViewportWidth > newViewportWidth
    ) {
        leftValue -= totalMovementSize;
        cCarouselInner.style.left = leftValue + "px";
        oldViewportWidth = newViewportWidth;
    }
}