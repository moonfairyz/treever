var pos;

var $demo;

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    $demo.text("Geolocation is not supported by this browser.");
  }
}

function showPosition(position) {
  pos = position;
  var { latitude, longitude } = pos.coords;
  $demo.html(`Latitude: ${latitude}<br>Longitude: ${longitude}`);
  $('#btn_submit').attr("disabled", null);
}

$(document).ready(function() {
  $demo = $("#demo");
  $('#btn_submit').on('click', function() {
    var data = pos.coords;
    data.csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
    $.post("/shop/create_product", data, function() {
      alert("Saved Data!");
    });
  });
});

