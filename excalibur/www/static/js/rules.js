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
  $('#rule_upload').on('change', function () {
    var data = new FormData();
    // TODO: add support to upload multiple files
    $.each($('#rule_upload')[0].files, function (i, file) {
      data.append('file-' + i, file);
    });
    $.ajax({
      url: '/rules',
      type: 'POST',
      cache: false,
      contentType: false,
      data: data,
      processData: false,
      success: function (data) {
        window.location.reload();
      }
    });
  });
});
