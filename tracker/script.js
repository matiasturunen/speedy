'use strict';

// Please go and create your own token!!
mapboxgl.accessToken = 'pk.eyJ1IjoibWF0aWFzdHVydW5lbiIsImEiOiJjamlzeXFyMnUwOTh3M2puenAyazk4eHJmIn0.v3wbeuxctozDlFa92O_cHw';
const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v9'
});

const dropArea = document.getElementById('fileupload');
const coordinates = [];

function preventDefaults(e) {
  e.preventDefault();
  e.stopPropagation();
}

function highlight() {
  dropArea.classList.add('highlight');
}

function unhighlight() {
  dropArea.classList.remove('highlight');
}

function handleDrop(e) {
  const dt = e.dataTransfer
  const files = dt.files

  const file = files[0]

  const reader = new FileReader();
  reader.onload = event => {
    const data = event.target.result;
    data.split('\n').forEach(row => {
      const coords = row.split(';');
      coordinates.push({
        lat: coords[0],
        lon: coords[1],
        time: coords[2]
      });
    };
  };
  reader.readAsText(file)
}

function toRad(x) {
  return x * Math.PI / 180;
}

function haversine(lat1, lon1, lat2, lon2) {
  // Calculate distance between two points
  const dlon = lon2 - lon1;
  const dlat = lat2 - lat1;
  const R = 6371; // km 
  
  dLat = toRad(dLat)
  dLon = toRad(dLon)  
  const a = Math.sin(dLat/2) * Math.sin(dLat/2) + 
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * 
    Math.sin(dLon/2) * Math.sin(dLon/2);  
  
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
  const d = R * c;

  return d;
}

function getSpeed(lat1, lon1, lat2, lon2, time) {
  return haversine(lat1, lon1, lat2, lon2) / time;
}

function processGPSTrack() {
  let topSpeed = 0;
  const speeds = [];
  let averageSpeed = 0;
  let distance = 0;

  let prevtime = 0
  let prevLat = 0;
  let prevLon = 0;
  coordinates.forEach(coords => {
    if (prevtime == 0) {
      prevtime = coords.time;
      prevLat = coords.lat;
      prevLon = coords.lon;
    } else {
      const timeDelta = coords.time - prevtime;
      distance = distance + haversine(prevLat, prevLon, coords.lat, coords.lon);
      const spd = getSpeed(prevLat, prevLon, coords.lat, coords.lon, timeDelta);
      speeds.push(spd);
      if (spd > topSpeed) {
        topSpeed = spd;
      }

      // Create map marker
      

      prevtime = coords.time;
      prevLat = coords.lat;
      prevLon = coords.lon;
    }
  });
}

// Add events for droparea
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => dropArea.addEventListener(eventName, preventDefaults, false));
['dragenter', 'dragover'].forEach(eventName => dropArea.addEventListener(eventName, highlight, false));
['dragleave', 'drop'].forEach(eventName => dropArea.addEventListener(eventName, unhighlight, false));
dropArea.addEventListener('drop', handleDrop, false);