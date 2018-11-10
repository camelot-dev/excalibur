// https://coderwall.com/p/flonoa/simple-string-format-in-javascript
String.prototype.format = function () {
  var str = this;
  for (var i in arguments) {
    str = str.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
  }
  return str;
}

const onRuleDownload = (elRef) => {
  const ruleId = elRef.getAttribute('data-rule-id');
  console.log({type: 'hidden', name: 'rule_id', val: ruleId});
  // $.ajax({
  //   url: '/download/rule',
  //   type: 'POST',
  //   cache: false,
  //   contentType: false,
  //   data: {type: 'hidden', name: 'rule_id', val: ruleId},
  //   processData: false,
  //   success: function (data) {
  //     console.log(data)
  //     // window.location.replace(redirect);
  //   }
  // });
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
