// Initialize and add the map
function myMap() {
  const myLatLng = { lat: 38.044660, lng: 23.743526 };
  const map = new google.maps.Map(document.getElementById("map"), {
    center:myLatLng,
    zoom:17,
  });

new google.maps.Marker({
  position: new google.maps.LatLng(38.044660,23.743526),
  map: map,
  title: "Hello World!",

});
}
// Api Key: AIzaSyBIwzALxUPNbatRBj3Xi1Uhp0fFzwWNBkE
