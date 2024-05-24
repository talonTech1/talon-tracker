<script>
    const openSidebarButton = document.querySelector('.open-sidebar-button');
    const sidebar = document.querySelector('.sidebar');
    const setAvailabilityButton = document.getElementById('set-availability-button');
    const availabilityPopup = document.getElementById('availability-popup');
    const locationPopup = document.getElementById('location-popup');
    const overlay = document.querySelector('.overlay');
    const locationDivs = document.querySelectorAll('.location, .favorite');
    const cancelButtons = document.querySelectorAll('.cancel');

    openSidebarButton.addEventListener('click', () => {
        sidebar.classList.toggle('open');
    });

    setAvailabilityButton.addEventListener('click', () => {
        availabilityPopup.style.display = 'block';
        overlay.style.display = 'block';
    });

    locationDivs.forEach(locationDiv => {
        locationDiv.addEventListener('click', () => {
            locationPopup.style.display = 'block';
            overlay.style.display = 'block';
        });
    });

    cancelButtons.forEach(cancelButton => {
        cancelButton.addEventListener('click', () => {
            availabilityPopup.style.display = 'none';
            locationPopup.style.display = 'none';
            overlay.style.display = 'none';
        });
    });

    overlay.addEventListener('click', () => {
        availabilityPopup.style.display = 'none';
        locationPopup.style.display = 'none';
        overlay.style.display = 'none';
    });

    // Example function to add a location
    function addLocation(locationN, fav = false) {
        fetch('http://127.0.0.1:5000/add_location', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ locationN: locationN, fav: fav })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error', error);
        });
    }

    // Call addLocation function when needed
    // addLocation('Loc 7', true);
</script>