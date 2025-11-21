// Initialize Socket.IO
const socket = io();

// DOM Elements
const logContainer = document.getElementById('log-feed');
const counterElem = document.getElementById('total-attacks');
let totalAttacks = 0;

// Audio Context for sound effects
const alertSound = new Audio('/static/sounds/alert.wav');

// Connection Status
socket.on('connect', () => {
    console.log("Connected to Watchtower Core");
    addLogEntry({
        timestamp: new Date().toLocaleTimeString(),
        src_ip: "SYSTEM",
        country: "LOC",
        payload: "Connection established. Monitoring active...",
        severity: "low"
    });
});

// Handle New Logs
socket.on('new_log', (data) => {
    // 1. Update Stats
    totalAttacks++;
    if(counterElem) counterElem.innerText = totalAttacks;

    // 2. Play Sound if High Severity
    if (data.severity === 'high' || data.severity === 'critical') {
        alertSound.play().catch(e => console.log("Audio play failed (interaction needed)"));
    }

    // 3. Update Map (Function defined in map.js)
    if (window.updateMapMarker) {
        window.updateMapMarker(data);
    }

    // 4. Add to Log List
    addLogEntry(data);
});

function addLogEntry(data) {
    const div = document.createElement('div');
    div.className = `log-entry severity-${data.severity || 'low'}`;
    
    // HTML Template for a single row
    div.innerHTML = `
        <span class="log-time">[${data.timestamp || new Date().toLocaleTimeString()}]</span>
        <span class="log-ip">${data.src_ip}</span>
        <span class="log-country">${data.iso_code || 'XX'}</span>
        <span class="log-payload">${escapeHtml(data.payload || '')}</span>
    `;

    // Add to top
    logContainer.insertBefore(div, logContainer.firstChild);

    // Limit to 50 entries to prevent browser lag
    if (logContainer.children.length > 50) {
        logContainer.removeChild(logContainer.lastChild);
    }
}

// Security: Prevent XSS in payloads
function escapeHtml(text) {
    if (!text) return "";
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}