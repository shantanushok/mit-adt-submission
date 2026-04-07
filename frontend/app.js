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

            setupWebSocket();
        } catch (error) {
            loader.classList.add('hidden');
            connectBtn.classList.remove('hidden');
            connectBtn.textContent = 'Retry Connection';
            statusText.textContent = 'Backend Not Responding (Check console)';
            console.error('Connection error:', error);
        }
    });

    function setupWebSocket() {
        const ws = new WebSocket('ws://localhost:8000/api/ws/stream');
        
        ws.onopen = () => {
            console.log('WebSocket Connected');
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            // Update Stat Cards
            document.getElementById('kafka-value').textContent = data.kafka_events.toLocaleString();
            document.getElementById('db-value').textContent = data.db_documents.toLocaleString();
            document.getElementById('last-event').textContent = data.last_event;

            // Plot on Chart
            updateChart(data);
        };

        ws.onerror = (err) => console.error('WS Error:', err);
        ws.onclose = () => console.log('WS Disconnected');
    }

    // Chart.js Configuration
    const ctx = document.getElementById('telemetryChart').getContext('2d');
    
    // Set global default color to readable light text
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.font.family = 'Inter';

    const telemetryChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'CPU Usage (%)',
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    borderWidth: 2,
                    data: [],
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Memory Usage (%)',
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    borderWidth: 2,
                    data: [],
                    tension: 0.4,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: { color: 'rgba(255,255,255,0.05)' }
                },
                x: {
                    grid: { color: 'rgba(255,255,255,0.05)' }
                }
            },
            plugins: {
                legend: {
                    labels: { color: '#f8fafc' }
                }
            }
        }
    });

    const MAX_DATA_POINTS = 20;

    function updateChart(data) {
        if (telemetryChart.data.labels.length >= MAX_DATA_POINTS) {
            telemetryChart.data.labels.shift();
            telemetryChart.data.datasets[0].data.shift();
            telemetryChart.data.datasets[1].data.shift();
        }
        
        telemetryChart.data.labels.push(data.timestamp);
        telemetryChart.data.datasets[0].data.push(data.cpu);
        telemetryChart.data.datasets[1].data.push(data.memory);
        
        telemetryChart.update();
    }
});
