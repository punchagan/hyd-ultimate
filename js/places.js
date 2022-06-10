const setupSearchBox = () => {
  const inputBox = document.querySelector("#inputLocality");
  const defaultBounds = new google.maps.LatLngBounds(
    new google.maps.LatLng(17.1867065, 78.5185524),
    new google.maps.LatLng(17.1867065, 78.5185524)
  );
  const searchBox = new google.maps.places.SearchBox(inputBox, {
    // Doesn't restrict the results, but changes the ordering...
    bounds: defaultBounds
  });

  const updateLocation = () => {
    const location = searchBox.getPlaces()[0];
    if (location) {
      const coords = {
        lat: location.geometry.location.lat(),
        lng: location.geometry.location.lng()
      };
      console.log(coords);
      const locationBox = document.querySelector("#inputLocation");
      const text = `${coords.lat},${coords.lng}`;
      locationBox.value = text;
    }
  };
  google.maps.event.addListener(searchBox, "places_changed", updateLocation);
};

window.setupSearchBox = setupSearchBox;
