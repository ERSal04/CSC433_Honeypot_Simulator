// Wait for DOM to load
document.addEventListener('DOMContentLoaded', () => {
    
    // 1. Initialize Leaflet Map
    // 'map-container' must exist in the HTML
    const map = L.map('map-container').setView([20, 0], 2); // Center on world

    // 2. Add Dark Tiles (Free from CartoDB)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 19
    }).addTo(map);

    // Store markers so we can remove them later
    const markers = [];

    // 3. Define Global Update Function
    // This is called by live_feed.js when a socket event comes in
    window.updateMapMarker = function(data) {
        if (!data.latitude || !data.longitude) return;

        // Create Marker
        const lat = data.latitude;
        const lng = data.longitude;

        // Different color for High Severity
        const color = (data.severity === 'high') ? '#ef4444' : '#10b981';

        // Custom Circle Marker
        const circle = L.circleMarker([lat, lng], {
            color: color,
            fillColor: color,
            fillOpacity: 0.5,
            radius: 5
        }).addTo(map);

        // Add Popup
        circle.bindPopup(`
            <b>${data.src_ip}</b><br>
            ${data.city}, ${data.country}<br>
            Payload: ${data.payload ? data.payload.substring(0, 20) : 'N/A'}...
        `);

        // Pulse effect (simple implementation: open popup briefly)
        // circle.openPopup(); 
        // setTimeout(() => circle.closePopup(), 2000);

        // Manage Marker Array (Limit to 20 on map to keep it clean)
        markers.push(circle);
        if (markers.length > 20) {
            const oldMarker = markers.shift();
            map.removeLayer(oldMarker);
        }
    };
});