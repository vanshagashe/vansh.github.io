document.getElementById("getLocationBtn").addEventListener("click", function() {
    getLocation();
});

function getLocation() {
    document.getElementById("loading").style.display = "block";
    document.getElementById("result").style.display = "none";
    
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function showPosition(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;

    // Send coordinates to backend
    fetch('http://localhost:5000/find_nearest_tutors', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ latitude: lat, longitude: lon })
    })
    .then(response => response.json())
    .then(data => {
        displayTutors(data);
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Unable to fetch tutors. Please try again later.");
    });
}

function showError(error) {
    document.getElementById("loading").style.display = "none";
    switch(error.code) {
        case error.PERMISSION_DENIED:
            alert("User denied the request for Geolocation.");
            break;
        case error.POSITION_UNAVAILABLE:
            alert("Location information is unavailable.");
            break;
        case error.TIMEOUT:
            alert("The request to get user location timed out.");
            break;
        case error.UNKNOWN_ERROR:
            alert("An unknown error occurred.");
            break;
    }
}

function displayTutors(tutors) {
    document.getElementById("loading").style.display = "none";
    document.getElementById("result").style.display = "block";

    const tutorList = document.getElementById("tutorList");
    tutorList.innerHTML = "";  // Clear previous results

    tutors.forEach((tutor, index) => {
        const li = document.createElement("li");
        // Each tutor links to a portfolio page (using their name as a unique identifier)
        li.innerHTML = `<a href="portfolio.html?id=${tutor.name}" target="_blank">${index + 1}. ${tutor.name} - ${tutor.distance.toFixed(2)} km</a>`;
        tutorList.appendChild(li);
    });
}
