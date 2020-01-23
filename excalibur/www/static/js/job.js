const pollUntilServerIsReady = function () {
  window.setInterval(() => {
    const httpRequest = new XMLHttpRequest();
    httpRequest.onloadend = () => {
      if (httpRequest.status < 300) {
        if(httpRequest.responseText.indexOf('__please-wait-symbol__') == -1) {
          window.location.reload(true); 
        }
      } 
    };
    
    httpRequest.open("GET", window.location);
    httpRequest.send();
  }, 500);
};

$(document).ready(function () {

  if(document.getElementById('__please-wait-symbol__') != null) {
    pollUntilServerIsReady();
  }

  var loc = window.location.pathname.split('/');

  $('#download').click(function () {
    var input = $('<input>', {type: 'hidden', name: 'job_id', val: loc[loc.length - 1]});
    $('#download-form').append($(input));
    $('#download-form').submit();
  });
});