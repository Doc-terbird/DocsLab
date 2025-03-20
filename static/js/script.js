document.addEventListener('DOMContentLoaded', () => {
    const fearGreedIndicator = document.getElementById('fear-greed-indicator');
    const fearGreedLevel = document.getElementById('fear-greed-level');
    const fearGreedContainer = document.getElementById('fear-greed-container');

    function updateFearGreedIndex() {
        // Simulated Fear & Greed Index (replace with real API in future)
        const currentIndex = Math.floor(Math.random() * 100);
        const percentage = Math.min(Math.max(currentIndex, 0), 100);
        
        fearGreedLevel.style.height = `${percentage}%`;
        
        // Color and tooltip logic
        if (percentage <= 20) {
            fearGreedLevel.style.backgroundColor = '#DC3545';
            fearGreedIndicator.setAttribute('title', `Extreme Fear (${percentage})`);
        } else if (percentage <= 40) {
            fearGreedLevel.style.backgroundColor = '#FF6B6B';
            fearGreedIndicator.setAttribute('title', `Fear (${percentage})`);
        } else if (percentage <= 60) {
            fearGreedLevel.style.backgroundColor = '#FFC107';
            fearGreedIndicator.setAttribute('title', `Neutral (${percentage})`);
        } else if (percentage <= 80) {
            fearGreedLevel.style.backgroundColor = '#4CAF50';
            fearGreedIndicator.setAttribute('title', `Greed (${percentage})`);
        } else {
            fearGreedLevel.style.backgroundColor = '#28A745';
            fearGreedIndicator.setAttribute('title', `Extreme Greed (${percentage})`);
        }
    }

    // Update Fear & Greed Index every 5 seconds
    updateFearGreedIndex();
    setInterval(updateFearGreedIndex, 5000);

    // Draggable Fear & Greed Widget
    let isDragging = false;
    let currentX;
    let currentY;
    let initialX;
    let initialY;
    let xOffset = 0;
    let yOffset = 0;

    fearGreedContainer.addEventListener('mousedown', dragStart);
    document.addEventListener('mousemove', drag);
    document.addEventListener('mouseup', dragEnd);

    function dragStart(e) {
        initialX = e.clientX - xOffset;
        initialY = e.clientY - yOffset;

        if (e.target === fearGreedContainer) {
            isDragging = true;
            fearGreedContainer.style.opacity = '0.7';
        }
    }

    function drag(e) {
        if (isDragging) {
            e.preventDefault();
            currentX = e.clientX - initialX;
            currentY = e.clientY - initialY;

            xOffset = currentX;
            yOffset = currentY;

            setTranslate(currentX, currentY, fearGreedContainer);
        }
    }

    function dragEnd(e) {
        initialX = currentX;
        initialY = currentY;

        isDragging = false;
        fearGreedContainer.style.opacity = '1';

        // Save widget position to localStorage
        localStorage.setItem('fearGreedWidgetPosition', JSON.stringify({x: xOffset, y: yOffset}));
    }

    function setTranslate(xPos, yPos, el) {
        el.style.transform = `translate3d(${xPos}px, ${yPos}px, 0)`;
    }

    // Restore widget position from localStorage on page load
    const savedPosition = localStorage.getItem('fearGreedWidgetPosition');
    if (savedPosition) {
        const {x, y} = JSON.parse(savedPosition);
        xOffset = x;
        yOffset = y;
        setTranslate(x, y, fearGreedContainer);
    }
});