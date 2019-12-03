mapboxgl.accessToken = 'pk.eyJ1Ijoibmdhbmh0YWthIiwiYSI6ImNrMmxxbTd3OTA1eHEzZW8yY3VvZjVxeGEifQ.8V-7GFmm1KEG2ZGtCgkdbw';

var url = "../lib/data_trans/voies_mel_draw_circle.geojson";

var map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/streets-v11',
  center: [3.0667, 50.6333],
  zoom: 15,
  pitch: 15,
  bearing: -17.6,
  //antialias: true
});

function inLine(a, b, c) {
  xmin = (a[0]<c[0]) ? a[0] : c[0];
  ymin = (a[1]<c[1]) ? a[1] : c[1];
  xmax = (a[0]>c[0]) ? a[0] : c[0];
  ymax = (a[1]>c[1]) ? a[1] : c[1];
  return (b[0]>=xmin && b[0]<=xmax && b[1]>=ymin && b[1]<=ymax);
}

function inRoute(p, route) {
  let founded=false;
  let i=0;
  while (!founded && i<route.length-1) {
    if (inLine(route[i], p, route[i+1])) founded=true;
    i++;
  }
  return founded;
}

map.on('load', function() {

  var directions =  new MapboxDirections({
    accessToken: mapboxgl.accessToken
  });
  map.addControl(directions, 'top-left');

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

  directions.on("route", e => {
    // routes is an array of route objects as documented here:
    // https://docs.mapbox.com/api/navigation/#route-object
    let routes = e.route[0].legs[0].steps.map(e => e.maneuver.location);
    
    var loaded = false;
    map.on('sourcedata', function(e) {
      if (loaded) return
      //if (e.sourceId !== 'total' && e.sourceId !== 'my_data') return
      if (e.isSourceLoaded !== true) return
      var features = map.queryRenderedFeatures({layers: ['total']}); 

      var data = {
        "type": "FeatureCollection",
        "features": []
      }
      
      features.forEach(function(f) {
        
        if (inRoute(f.geometry.coordinates, routes)) {
          var object = turf.centerOfMass(f)
          var center = object.geometry.coordinates
          var radius = 10;
          var options = {
            steps: 16,
            units: 'meters',
            properties: object.properties
          };
          data.features.push(turf.circle(center, radius, options))
        }
      })
      loaded = true;
      map.getSource('extrusion').setData(data);
    })
  })
});
