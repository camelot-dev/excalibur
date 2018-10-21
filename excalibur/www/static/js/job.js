$(document).ready(function () {
  var loc = window.location.pathname.split('/');

  $('#download').click(function () {
    var input = $('<input>', {type: 'hidden', name: 'job_id', val: loc[loc.length - 1]});
    $('#download-form').append($(input));
    $('#download-form').submit();
  });
});