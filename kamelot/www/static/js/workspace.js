// https://coderwall.com/p/flonoa/simple-string-format-in-javascript
String.prototype.format = function() {
  let str = this;
  for (let i in arguments) {
    str = str.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
  }
  return str;
}

const compare = function (a, b) {
  return a - b;
}

const translate = function (x1, x2) {
  x2 += x1;
  return x2;
}

const getScaleOffset = function (imgHeight, selectedArea, scalingFactorY) {
  const absArea = Math.abs(translate(-imgHeight, selectedArea));
  return absArea * scalingFactorY;
}

const getTransformArea = function (selectedArea, scalingFactorX, scalingFactorY, doTranslate, image_height) {
  let tArea = [];
  for (let i = 0; i < selectedArea.length; i++) {
    let x1 = selectedArea[i].x * scalingFactorX;
    let x2 = selectedArea[i].x * selectedArea[i].width, scalingFactorX;
    let y1 = selectedArea[i].y * scalingFactorY;
    let y2 = (selectedArea[i].y + selectedArea[i].height) * scalingFactorY;

    if (doTranslate) {
      y1 = getScaleOffset(image_height, selectedArea[i].y, scalingFactorY);
      y2 = getScaleOffset(image_height, (selectedArea[i].y + selectedArea[i].height), scalingFactorY);
    }
    tArea.push([x1, y1, x2, y2].join());
  }
  return tArea;
};

const getColumns = function (columns, scaling_factor_x) {
  let cols = [];

  columns.forEach(col => {
    cols.push(scale(col, scaling_factor_x));
  });
  cols.sort(compare);

  return cols.join();
};

const debugQtyAreas = function (event, id, areas) {
  return;
};

const getRuleOptions = function () {
  let ruleOptions = {};
  const flavor = $('#flavors').val();
  ruleOptions['flavor'] = flavor;
  const selectedAreas = $('#image').selectAreas('areas');
  const image_width = $('#image').width();
  const image_height = $('#image').height();
  const scalingFactorX = file_dimensions[0] / image_width;
  const scalingFactorY = file_dimensions[1] / image_height;
  const hasColumnSeparator = $('.draggable-column').length > 0;

  if (selectedAreas.length > 0) {
    ruleOptions['table_area'] = getTransformArea(selectedAreas, scalingFactorX, scalingFactorY, true, image_height);
  } else {
    ruleOptions['table_area'] = null;
  }

  switch(flavor.toString().toLowerCase()) {
    case 'lattice': {
      ruleOptions['process_background'] = $("#process-background").val() ? true : false;
      ruleOptions['line_size_scaling'] = $('#line-size-scaling').val() ? Number($('#line-size-scaling').val()) : 15;
      ruleOptions['split_text'] = $("#split-text-l").val() ? true : false;
      ruleOptions['flag_size'] = $("#flag-size-l").val() ? true : false;
      break;
    }
    case 'stream': {
      ruleOptions['row_close_tol'] = $('#row-close-tol').val() ? Number($('#line-size-scaling').val()) : 2;
      ruleOptions['col_close_tol'] = $('#col-close-tol').val() ? Number($('#line-size-scaling').val()) : 0;
      ruleOptions['split_text'] = $("#split-text-s").val() ? true : false;
      ruleOptions['flag_size'] = $("#flag-size-s").val() ? true : false;

      if (hasColumnSeparator) {
        let cols = []
        $('.draggable-column').each(function (id, col) {
          cols.push(($(col).offset().left - $(col).parent().offset().left) + ($(col).width() / 2));
        });
        cols = getColumns(cols, scalingFactorX);
        ruleOptions['columns'] = [cols];
      } else {
        ruleOptions['columns'] = null;
      }
      break;
    }
    default: {
      break;
    }
  }
  return ruleOptions;
};

const extract = () => {
  const loc = window.location.pathname.split('/');
  const rule_options = getRuleOptions();
  $.ajax({
    url: '/jobs',
    data: {
      file_id: loc[loc.length - 1],
      page_numbers: $('#page-numbers').val() ? $('#page-numbers').val() : '1',
      rule_options: JSON.stringify(rule_options)
    },
    type: 'POST',
    success: (data) => {
      const redirectUrl = '{0}//{1}/jobs/{2}'.format(window.location.protocol, window.location.host, data['job_id']);
      window.location.replace(redirectUrl);
    },
    error: (error) => {
      console.error(error);
    }
  });
}

$(document).ready(function () {
  $('.image-area').selectAreas({
    onChanged: debugQtyAreas
  });

  $("select[name='flavors']").on('change', function () {
    if ($(this).val() == 'Lattice') {
      $('.stream').hide();
      $('.lattice').show();
    } else {
      $('.stream').show();
      $('.lattice').hide();
    }
  });

  $('body').on('click', '.add-separator', function () {
    const position = $('#image-div').position();
    const column = $('<div>', {
      class: 'draggable-column'
    });
    $(column).css({
      'position': 'absolute',
      'top': position.top,
      'left': position.left + 20,
      'background-color': 'blue',
      'height': $('#image-div').height(),
      'width': '4px',
      'z-index': 200
    });
    $('#image-div').append(column);
    $('.draggable-column').draggable({
      axis: 'x',
      containment: 'parent'
    });
  });

  $('body').on('dblclick', '.draggable-column', function () {
    $(this).remove();
  });
});
