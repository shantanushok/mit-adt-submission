document.addEventListener('DOMContentLoaded', () => {
    const connectBtn = document.getElementById('connect-btn');
    const statusText = document.getElementById('api-status-text');
    const statusIndicator = document.getElementById('api-status-indicator');
    const loader = document.getElementById('api-loader');

    // Mocks connection process until API setup is complete
    connectBtn.addEventListener('click', async () => {
        // UI Loading state
        connectBtn.classList.add('hidden');
        loader.classList.remove('hidden');
        try {
            statusText.textContent = 'Attempting API connection...';
            const response = await fetch('http://localhost:8000/api/health');
            const data = await response.json();
            
            loader.classList.add('hidden');
            statusText.textContent = 'API Connected successfully!';
            statusIndicator.classList.remove('disconnected');
            statusIndicator.classList.add('connected');
            connectBtn.classList.add('hidden');
        } catch (error) {
            loader.classList.add('hidden');
            connectBtn.classList.remove('hidden');
            connectBtn.textContent = 'Retry Connection';
            statusText.textContent = 'Backend Not Responding (Check console)';
            console.error('Connection error:', error);
        }
    });
});
