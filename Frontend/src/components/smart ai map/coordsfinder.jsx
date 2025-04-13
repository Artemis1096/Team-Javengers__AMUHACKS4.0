import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

function CoordsFinder() {
  const [coords, setCoords] = useState({ lat: 51.505, lng: -0.09 });
  const navigate = useNavigate();

  // Function to update coordinates
  const updateCoordinates = (lat, lng) => {
    setCoords({ lat, lng });
  };

  // Function to handle button click to store coords and navigate
  const handleNextPage = () => {
    // Store coordinates in a variable (e.g., using state or a global state manager)
    localStorage.setItem('lat', coords.lat);
    localStorage.setItem('lng', coords.lng);

    // Navigate to the next page
    navigate('/next');
  };

  // Initialize the map when the component is mounted
  React.useEffect(() => {
    const map = L.map('map').setView([51.505, -0.09], 13);

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Create a draggable marker
    const marker = L.marker([51.505, -0.09], { draggable: true }).addTo(map);

    // Initial popup content
    marker.bindPopup(`Lat: 51.505, Lng: -0.09`).openPopup();

    // Event listener for when the marker is dragged
    marker.on('dragend', function(event) {
      const position = marker.getLatLng();
      updateCoordinates(position.lat, position.lng);
      map.panTo(position); // Optional: Center map on new marker position
    });

    // Event listener for clicking on the map to move the marker
    map.on('click', function(event) {
      marker.setLatLng(event.latlng);
      updateCoordinates(event.latlng.lat, event.latlng.lng);
    });

    return () => {
      map.remove(); // Cleanup map on unmount
    };
  }, []);

  return (
    <div className="App">
      <div id="map" style={{ height: '500px', width: '100%' }}></div>
      <div id="coords" style={{ marginTop: '10px', fontFamily: 'Arial, sans-serif', fontSize: '16px' }}>
        Latitude: {coords.lat.toFixed(5)}, Longitude: {coords.lng.toFixed(5)}
      </div>
      <button onClick={handleNextPage} style={{ marginTop: '20px' }}>
        Go to Next Page
      </button>
    </div>
  );
}

export default CoordsFinder;
