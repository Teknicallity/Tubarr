export function initializeCarousel() {
    const carouselInner = document.getElementById('video-carousel-inner');
    const prevBtn = document.getElementById('prev-video-btn');
    const nextBtn = document.getElementById('next-video-btn');

    let carouselVp = document.querySelector(".carousel-viewport");
    let cCarouselInner = document.querySelector(".carousel-track");
    let carouselInnerWidth = cCarouselInner.getBoundingClientRect().width;
    let carouselItem = document.querySelector(".carousel-item");
    let leftValue = 0;
    cCarouselInner.style.left = leftValue + "px";

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
        let newVidHtml = newVideos.map(video => carouselInner.innerHTML += `
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
        `)
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
        if (!(leftValue === 0)) {
            leftValue -= -getTotalMovementSize();
            cCarouselInner.style.left = leftValue + "px";
        }
        if (leftValue > 0) {
            leftValue = 0;
            cCarouselInner.style.left = leftValue + "px";
        }
        updateButtons()
    });

    nextBtn.addEventListener("click", () => {
        currentIndex = (currentIndex + displayAmount < videos.length) ? currentIndex + displayAmount : currentIndex;
        const carouselVpWidth = carouselVp.getBoundingClientRect().width;
        console.log('carouselInnerWidth', carouselInnerWidth)
        console.log('carouselVpWidth', carouselVpWidth)
        console.log('calulation', carouselInnerWidth, '-', leftValue, '>', carouselVpWidth)
        console.log('res', carouselInnerWidth - Math.abs(leftValue), '>', carouselVpWidth)
        if (carouselInnerWidth - Math.abs(leftValue) > carouselVpWidth) {
            console.log('before', leftValue);
            leftValue -= getTotalMovementSize();
            console.log('after', leftValue);
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
        }
        updateButtons();
    });

    const mediaQuery500 = window.matchMedia("(max-width: 500px)");
    const mediaQuery750 = window.matchMedia("(max-width: 750px)");
    const mediaQuery980 = window.matchMedia("(max-width: 980px)");
    const mediaQuery1150 = window.matchMedia("(max-width: 1150px)");
    const mediaQuery1430 = window.matchMedia("(max-width: 1430px)");
    const mediaQuery1700 = window.matchMedia("(max-width: 1700px)");
    const mediaQuery2000 = window.matchMedia("(max-width: 2000px)");
    const mediaQuery2200 = window.matchMedia("(max-width: 2200px)");

    mediaQuery500.addEventListener("change", mediaManagement);
    mediaQuery750.addEventListener("change", mediaManagement);
    mediaQuery980.addEventListener("change", mediaManagement);
    mediaQuery1150.addEventListener("change", mediaManagement);
    mediaQuery1430.addEventListener("change", mediaManagement);
    mediaQuery1700.addEventListener("change", mediaManagement);
    mediaQuery2000.addEventListener("change", mediaManagement);
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
}