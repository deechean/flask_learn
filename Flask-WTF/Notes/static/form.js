const response = fetch(url, {
    method: 'POST',
    headers:{
        'X-CSRToken': document.getElementById('csrf_token').value,
        'Cotent-Type': 'application/x-www-form-urlencoded'
    },
    body:
})