document.addEventListener('DOMContentLoaded', () => {
    const economicIndicators = {
        unemployment: {
            valueElement: document.querySelector('.economic-unemployment'),
            trendElement: document.querySelector('.economic-unemployment-trend')
        },
        inflation: {
            valueElement: document.querySelector('.economic-inflation'),
            trendElement: document.querySelector('.economic-inflation-trend')
        },
        interestRate: {
            valueElement: document.querySelector('.economic-interest-rate'),
            trendElement: document.querySelector('.economic-interest-rate-trend')
        }
    };

    async function fetchEconomicIndicators() {
        try {
            const response = await fetch('/api/economic-indicators');
            const data = await response.json();

            // Update Unemployment
            economicIndicators.unemployment.valueElement.textContent = 
                `${data.unemployment.value.toFixed(2)}%`;
            economicIndicators.unemployment.trendElement.textContent = 
                `${data.unemployment.change_percent.toFixed(2)}% ${data.unemployment.trend}`;
            economicIndicators.unemployment.trendElement.classList.remove('text-green-500', 'text-red-500');
            economicIndicators.unemployment.trendElement.classList.add(
                data.unemployment.trend === 'positive' ? 'text-green-500' : 'text-red-500'
            );

            // Update Inflation
            economicIndicators.inflation.valueElement.textContent = 
                `${data.inflation.value.toFixed(2)}%`;
            economicIndicators.inflation.trendElement.textContent = 
                `${data.inflation.change_percent.toFixed(2)}% ${data.inflation.trend}`;
            economicIndicators.inflation.trendElement.classList.remove('text-green-500', 'text-red-500');
            economicIndicators.inflation.trendElement.classList.add(
                data.inflation.trend === 'positive' ? 'text-green-500' : 'text-red-500'
            );

            // Update Interest Rate
            economicIndicators.interestRate.valueElement.textContent = 
                `${data.interest_rate.value.toFixed(2)}%`;
            economicIndicators.interestRate.trendElement.textContent = 
                `${data.interest_rate.change_percent.toFixed(2)}% ${data.interest_rate.trend}`;
            economicIndicators.interestRate.trendElement.classList.remove('text-green-500', 'text-red-500');
            economicIndicators.interestRate.trendElement.classList.add(
                data.interest_rate.trend === 'positive' ? 'text-green-500' : 'text-red-500'
            );
        } catch (error) {
            console.error('Error fetching economic indicators:', error);
        }
    }

    // Fetch indicators immediately and then every hour
    fetchEconomicIndicators();
    setInterval(fetchEconomicIndicators, 3600000);  // 1 hour
});