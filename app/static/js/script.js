function sendClick(adId) {
    fetch('/click', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ ad_id: adId })
    });
}
