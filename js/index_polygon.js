mapboxgl.accessToken = "pk.eyJ1Ijoibmdhbmh0YWthIiwiYSI6ImNrMmxxbTd3OTA1eHEzZW8yY3VvZjVxeGEifQ.8V-7GFmm1KEG2ZGtCgkdbw";

var map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/streets-v10',
  center: [3.0667, 50.6333],
  zoom: 14,
  pitch: 40,
  bearing: 20,
  antialias: true
});

map.on('load', function() {
  map.addLayer({
    'id': 'room-extrusion',
    'type': 'fill-extrusion',
    'source': {
      'type': 'geojson',
      'data': '../lib/data_trans/voies_mel_draw_polygon.geojson'
    },
    'paint': {
      'fill-extrusion-color': ['get', 'color'],
      'fill-extrusion-height': ['get', 'height'],
      
      // Get fill-extrusion-base from the source 'base_height' property.
      'fill-extrusion-base': 30,
      
      // Make extrusions slightly opaque for see through indoor walls.
      'fill-extrusion-opacity': 0.7
    }
  });
});
