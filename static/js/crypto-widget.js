document.addEventListener('DOMContentLoaded', () => {
    const cryptoCards = document.querySelectorAll('.crypto-card');
    const cryptoSymbols = ['BTC', 'ETH', 'BNB', 'ADA', 'SOL'];

    async function fetchCryptoPrices() {
        try {
            const response = await fetch('/api/crypto-prices');
            const data = await response.json();

            cryptoCards.forEach((card, index) => {
                const symbol = cryptoSymbols[index];
                const priceElement = card.querySelector('.crypto-price');
                const changeElement = card.querySelector('.crypto-change');

                if (data[symbol]) {
                    const price = data[symbol].price;
                    const change = data[symbol].change;

                    priceElement.textContent = `$${price.toFixed(2)}`;
                    changeElement.textContent = `${change >= 0 ? '+' : ''}${change.toFixed(2)}%`;
                    changeElement.classList.remove('text-[#DC3545]', 'text-[#28A745]');
                    changeElement.classList.add(change >= 0 ? 'text-[#28A745]' : 'text-[#DC3545]');
                }
            });
        } catch (error) {
            console.error('Error fetching crypto prices:', error);
        }
    }

    // Fetch prices immediately and then every 10 seconds
    fetchCryptoPrices();
    setInterval(fetchCryptoPrices, 10000);
});