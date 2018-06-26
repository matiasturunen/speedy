//'use strict';

// Please go and create your own token!!
mapboxgl.accessToken = 'pk.eyJ1IjoibWF0aWFzdHVydW5lbiIsImEiOiJjamlzeXFyMnUwOTh3M2puenAyazk4eHJmIn0.v3wbeuxctozDlFa92O_cHw';
const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v9'
});

const geojson = {
  "type": "FeatureCollection",
  "features": [{
    "type": "Feature",
    "geometry": {
      "type": "LineString",
      "coordinates": [
      ]
    }
  }]
};


const mapPoints = {
  "type": "FeatureCollection",
  "features": []
};

const dropArea = $('#fileupload');

function preventDefaults(e) {
  e.preventDefault();
  e.stopPropagation();
}

function highlight() {
  dropArea.addClass('highlight');
}

function unhighlight() {
  dropArea.removeClass('highlight');
}

function handleDrop(e) {
  const dt = e.originalEvent.dataTransfer;
  const files = dt.files;
  const file = files[0];
  const coordinates = [];
  const reader = new FileReader();

  let firstRow = true;
  
  reader.onload = event => {
    const data = event.target.result;
    data.split('\n').forEach(row => {
      if (firstRow) { // skip first row that contains headers
        firstRow = false;
      } else {
        const coords = row.split(';');
        if (coords.length == 3) {
          coordinates.push({
            lat: coords[0],
            lon: coords[1],
            time: coords[2]
          });
        }
      }
    });
    processGPSTrack(coordinates);
  };
  reader.readAsText(file)
}

function toRad(x) {
  return x * Math.PI / 180;
}

function haversine(lat1, lon1, lat2, lon2) {
  // Calculate distance between two points
  let dLat = lat2 - lat1;
  let dLon = lon2 - lon1;
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
  return haversine(lat1, lon1, lat2, lon2)*1000 / time;
}

function average(arr) {
  let sum = 0;
  arr.forEach(i => sum+= i);
  return sum/arr.length;
}

function processGPSTrack(coordinates) {
  let topSpeed = 0;
  const speeds = [];
  let averageSpeed = 0;
  let distance = 0;
  let totalTime = 0;

  let prevtime = 0
  let prevLat = 0;
  let prevLon = 0;

  const topSpeedLabel = $('#topSpeed');
  const avgSpeedLabel = $('#averageSpeed');
  const distanceLabel = $('#distance');
  const totalTimeLabel = $('#totalTime');

  let topSpeedLocation = { lat: 0, lon: 0 }

  coordinates.forEach(coords => {
    if (prevtime == 0) {
      prevtime = coords.time;
      prevLat = coords.lat;
      prevLon = coords.lon;
    } else {
      const timeDelta = coords.time - prevtime;
      let dist = haversine(prevLat, prevLon, coords.lat, coords.lon);
      if (dist > 0) { // must do to avoid NaN values
        distance += dist;
      }

      const spd = getSpeed(prevLat, prevLon, coords.lat, coords.lon, timeDelta);
      if (spd > 0) {  // must do to avoid NaN values
        speeds.push(spd);
      }

      if (spd > topSpeed) {
        topSpeed = spd;
        topSpeedLocation = { lat: coords.lat, lon: coords.lon };
      }

      totalTime += timeDelta;
      
      prevtime = coords.time;
      prevLat = coords.lat;
      prevLon = coords.lon;
    }

  });
  drawRoute(coordinates);
  drawLocation(topSpeedLocation, 'Top speed achieved');

  // Update labels
  topSpeedLabel.html(topSpeed);
  avgSpeedLabel.html(average(speeds));
  distanceLabel.html(distance);
  totalTimeLabel.html(totalTime/3600);
}

function drawRoute(coordinates) {
  // Empty coordinates
  geojson.features[0].geometry.coordinates = [];
  
  // Center map to first coordinates
  map.jumpTo({ 'center': [coordinates[0].lon, coordinates[0].lat], 'zoom': 12 });

  // Draw route
  coordinates.forEach(coords => {
    geojson.features[0].geometry.coordinates.push([coords.lon, coords.lat]); // Note that coordinates here are lon,lat instead of lat,lon
  });

  map.getSource('route').setData(geojson);
}

function drawLocation(location, name) {
  mapPoints.features.push({
    "type": "Feature",
    "geometry": {
      "type": "Point",
      "coordinates": [ location.lon, location.lat ]
    },
      "properties": {
        "title": name,
        "icon": "marker"
      }
  });

  map.getSource('points').setData(mapPoints);
}

// Add events for droparea
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => dropArea.on(eventName, preventDefaults));
['dragenter', 'dragover'].forEach(eventName => dropArea.on(eventName, highlight));
['dragleave', 'drop'].forEach(eventName => dropArea.on(eventName, unhighlight));
dropArea.on('drop', handleDrop);

map.on('load', () => {
  map.addSource('route', {type: 'geojson', data: geojson});
  map.addLayer({
    'id': 'route',
    'type': 'line',
    'source': 'route',
    'layout': {
      'line-cap': 'round',
      'line-join': 'round'
    },
    'paint': {
      'line-color': '#ed6498',
      'line-width': 5,
      'line-opacity': .8
    }
  });

  map.addSource('points', {type: 'geojson', data: mapPoints})
  map.addLayer({
    'id': 'points',
    'type': 'symbol',
    'source': 'points',
    'layout': {
    },
    'paint': {
      'icon-color': '#e55e5e'
    }
  });
});