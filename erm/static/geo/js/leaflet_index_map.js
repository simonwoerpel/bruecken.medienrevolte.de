var map;
var ajaxRequest;
var plotlist;
var plotlayers=[];

function initmap() {
    // set up AJAX request
    ajaxRequest = GetXmlHttpObject();
    if (ajaxRequest == null) {
        alert ("This browser does not support HTTP Request");
        return;
    }
    
    function GetXmlHttpObject() {
        if (window.XMLHttpRequest) { return new XMLHttpRequest(); }
        if (window.ActiveXObject)  { return new ActiveXObject("Microsoft.XMLHTTP"); }
        return null;
    }
    
    
	// set up the map
	map = new L.Map('map_index', {
        attributionControl: false,
        fullscreenControl: true
    }).setView([51.3324, 8.4430], 9);

    L.tileLayer('http://map.bruecken.medienrevolte.de/{z}/{x}/{y}.png', {
        attribution: 'Karte realisiert von <a href="http://medienrevolte.de">medienrevolte.de</a>',
        maxZoom: 12,
        minZoom: 6
    }).addTo(map);
    

    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        minZoom: 13,
        maxZoom: 16,
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map); 
    
    function ZoomHandler() {
        var currentZoom = map.getZoom();
        switch (currentZoom) {
            case 13:
            case 14:
            case 15:
            case 16:
                askForMarkers();
                map.on('moveend', askForMarkers );
                break;
            default:
                removeMarkers();
                ajaxRequest.abort();
        }
    }


    map.on('zoomend', function (e) {
        ZoomHandler();
    });



    // detect fullscreen toggling
    map.on('enterFullscreen', function(){
        if(window.console) window.console.log('enterFullscreen');
    });
    map.on('exitFullscreen', function(){
        if(window.console) window.console.log('exitFullscreen');
    });
    
    
    function askForMarkers() {
        // request the marker info with AJAX for the current bounds
        var currentZoom = map.getZoom();
        var bounds = map.getBounds();
        var minll = bounds.getSouthWest();
        var maxll = bounds.getNorthEast();
        var msg = '/map/' + minll.lng + '/' + minll.lat + '/' + maxll.lng + '/' + maxll.lat + '/' + currentZoom;
        ajaxRequest.onreadystatechange = stateChanged;
        ajaxRequest.open('GET', msg, true);
        ajaxRequest.send(null);
    }
    
    
    function stateChanged() {
        // if AJAX returned a list of markers, add them to the map
        if (ajaxRequest.readyState == 4) {
            //use the info here that was returned
            if (ajaxRequest.status == 200) {
                plotlist=eval("(" + ajaxRequest.responseText + ")");
                removeMarkers();
                for (i=0;i<plotlist.length;i++) {
                    var plotll = new L.LatLng(plotlist[i].lat,plotlist[i].lon, true);
                    var plotmark = new L.Marker(plotll);
                    plotmark.data=plotlist[i];
                    map.addLayer(plotmark);
                    plotmark.bindPopup(plotlist[i].name+plotlist[i].details);
                    plotlayers.push(plotmark);
                }
            }
        }
    }

    function removeMarkers() {
        for (i=0;i<plotlayers.length;i++) {
            map.removeLayer(plotlayers[i]);
        }
        plotlayers=[];
    }

}


