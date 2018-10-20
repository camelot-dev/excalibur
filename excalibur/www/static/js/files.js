// https://coderwall.com/p/flonoa/simple-string-format-in-javascript
String.prototype.format = function() {
  var str = this;
  for (var i in arguments) {
    str = str.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
  }
  return str;
}

function formatDate(date) {
  var monthNames = [
    "January", "February", "March",
    "April", "May", "June", "July",
    "August", "September", "October",
    "November", "December"
  ];

  var day = date.getDate();
  var monthIndex = date.getMonth();
  var year = date.getFullYear();

  return day + ' ' + monthNames[monthIndex] + ' ' + year;
}


$(document).ready(function() {
  $('#file').on('change',function(){
    // get the file name
    const filename = document.getElementById("file").files[0].name;
    // replace the "Choose file..." label
    $(this).next('.uploadFile__label').html(filename);
  })

  $('#upload').on('click', function() {
    var data = new FormData();
    $.each($('#file')[0].files, function(i, file) {
      data.append('file-' + i, file);
    });
    var page_number = $('#page-number').val();
    data.append('page_number', page_number);
    $.ajax({
      url: '/files',
      type: 'POST',
      cache: false,
      contentType: false,
      data: data,
      processData: false,
      success: function (data) {
        var redirect = '{0}//{1}/workspaces/{2}'.format(window.location.protocol, window.location.host, data['file_id']);
        window.location.replace(redirect);
      }
    });
  });
});
