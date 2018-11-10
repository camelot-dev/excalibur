// https://coderwall.com/p/flonoa/simple-string-format-in-javascript
String.prototype.format = function () {
  var str = this;
  for (var i in arguments) {
    str = str.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
  }
  return str;
}

const onRuleDownload = (e) => {
  // https://stackoverflow.com/a/30800715/2780127
  const ruleName = e.nextElementSibling.getAttribute('data-rule-name');
  const ruleOptions = e.nextElementSibling.getAttribute('data-rule-options');
  const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(ruleOptions);
  e.nextElementSibling.setAttribute("href", dataStr);
  e.nextElementSibling.setAttribute("download", "{0}.json".format(ruleName));
  e.nextElementSibling.click();
}

$(document).ready(function () {
  $('#upload').on('click', function () {
    var data = new FormData();
    // TODO: add support to upload multiple files
    $.each($('#file')[0].files, function (i, file) {
      data.append('file-' + i, file);
    });
    var page_number = $('#page-number').val() ? Number($('#page-number').val()) : 1;
    data.append('page_number', page_number);
    // $.ajax({
    //   url: '/files',
    //   type: 'POST',
    //   cache: false,
    //   contentType: false,
    //   data: data,
    //   processData: false,
    //   success: function (data) {
    //     var redirect = '{0}//{1}/workspaces/{2}'.format(window.location.protocol, window.location.host, data['file_id']);
    //     window.location.replace(redirect);
    //   }
    // });
  });
});
