mapboxgl.accessToken = "pk.eyJ1Ijoibmdhbmh0YWthIiwiYSI6ImNrMmxxbTd3OTA1eHEzZW8yY3VvZjVxeGEifQ.8V-7GFmm1KEG2ZGtCgkdbw";

var url = "../lib/data_trans/comptages-routiers-sur-la-voirie-departementale_circle.geojson";

var map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/streets-v11',
  center: [3.0667, 50.6333],
  zoom: 15,
  pitch: 15,
  bearing: -17.6,
});

map.on('load', function() {

  map.addControl(new MapboxDirections({
    accessToken: mapboxgl.accessToken
  }), 'top-left');

  map.addSource("my_data", {
    type: "geojson",
    data: url
  });

  map.addLayer({
    'id': 'extrusion',
    'type': 'fill-extrusion',
    "source": {
      "type": "geojson",
      "data": {
        "type": "FeatureCollection",
        "features": []
      }
    },
    'paint': {
      'fill-extrusion-color': ['get', 'color'],
      'fill-extrusion-height': ['get', 'frequency'],
      'fill-extrusion-base': 0,
      'fill-extrusion-opacity': 0.7
    }
  });

  map.addLayer({
    'id': 'total',
    'type': 'circle',
    'paint': {
        'circle-radius': {
            'base': 1.75,
            'stops': [[12, 2], [22, 180]]
        },
        'circle-opacity' : 0
    },
    "source": 'my_data',
  });


  map.on('sourcedata', function(e) {
    if (e.isSourceLoaded !== true) return
    var features = map.queryRenderedFeatures({layers: ['total']}); 
    console.log(features);
    var data = {
      "type": "FeatureCollection",
      "features": []
    }
    
    features.forEach(function(f) {
      var object = turf.centerOfMass(f)
      var center = object.geometry.coordinates
      var radius = 10;
      var options = {
        steps: 16,
        units: 'meters',
        properties: object.properties
      };
      data.features.push(turf.circle(center, radius, options))
    })
    map.getSource('extrusion').setData(data);
  })  
  
});
