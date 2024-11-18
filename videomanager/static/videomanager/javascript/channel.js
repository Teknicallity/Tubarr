export function initializeCarousel({
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
