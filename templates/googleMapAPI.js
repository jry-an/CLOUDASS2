function addExistingMarkers() {
  //Individual access to elements
  var name0 = '{{route.checkpointlist[0].name}}';
  var lat0 = {{route.checkpointlist[0].latitude}};
  var long0 = {{route.checkpointlist[0].longitude}};
  var marker = new google.maps.Marker({
    position: new google.maps.LatLng({{ route.checkpointlist[0].latitude }}, {{ route.checkpointlist[0].longitude }}),
    map: map,
    title: '{{ route.checkpointlist[0].name }}'
  });

  //Trying to iterate over the list
  {% for checkpoint in route.checkpointlist %}
      var lat = checkpoint.latitude;
      var long = checkpoint.longitude;
      var cpname = checkpoint.name;
      var location = new google.maps.LatLng(lat, long);

      var marker = new google.maps.Marker({
            map: map,
            draggable:true,
            title:cpname,
            animation: google.maps.Animation.DROP,
            position: location,
      });
   {% end for %}
}