### Run :

> npm install mapbox-gl --save


### add your map to the site : 

    ```
    var mapboxgl = require('mapbox-gl/dist/mapbox-gl.js');
    
    mapboxgl.accessToken = 'pk.eyJ1Ijoibmdhbmh0YWthIiwiYSI6ImNrMmxxbTd3OTA1eHEzZW8yY3VvZjVxeGEifQ.8V-7GFmm1KEG2ZGtCgkdbw';
    var map = new mapboxgl.Map({
    container: 'YOUR_CONTAINER_ELEMENT_ID',
    style: 'mapbox://styles/mapbox/streets-v11'
    });
    ```

### Read more :
https://docs.mapbox.com/mapbox-gl-js/example/animate-a-line/