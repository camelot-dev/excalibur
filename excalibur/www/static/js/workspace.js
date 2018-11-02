let columnCountBuffer = 0;

// https://coderwall.com/p/flonoa/simple-string-format-in-javascript
String.prototype.format = function () {
  let str = this;
  for (let i in arguments) {
    str = str.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
  }
  return str;
}

const compare = function (a, b) {
  return a - b;
}

const doTranslateAndScale = function (relCoordinate, scalingFactorY) {
  const imageHeight = $('#image').height();
  const absCoordinate = Math.abs(relCoordinate - imageHeight);
  return absCoordinate * scalingFactorY;
}

const detectTableAreas = function(flavor) {
  const areaPadding = 2;
  const imageWidth = $('#image').width();
  const imageHeight = $('#image').height();
  const scalingFactorX = imageWidth / imageDim[0];
  const scalingFactorY = imageHeight / imageDim[1];

  let areaOptions = [];
  let x1, x2, y1, y2;
  for (let i = 0; detectedAreas[flavor].length; i++) {
    x1 = detectedAreas[flavor][i][0] * scalingFactorX;
    y1 = detectedAreas[flavor][i][1] * scalingFactorY;
    x2 = detectedAreas[flavor][i][2] * scalingFactorX;
    y2 = detectedAreas[flavor][i][3] * scalingFactorY;
    const areaOption = {
      x: Math.floor(x1) - areaPadding,
      y: Math.floor(y1) - areaPadding,
      width: Math.floor(Math.abs(x2 - x1)) + areaPadding,
      height: Math.floor(Math.abs(y2 - y1)) + areaPadding
    };
    areaOptions.push(areaOption);
  }
  return areaOptions;
};

const getTableAreas = function (selectedAreas, scalingFactorX, scalingFactorY, doTranslate) {
  let tArea = [];
  let x1, x2, y1, y2;
  for (let i = 0; i < selectedAreas.length; i++) {
    x1 = selectedAreas[i].x * scalingFactorX;
    x2 = selectedAreas[i].x * selectedAreas[i].width, scalingFactorX;
    y1 = selectedAreas[i].y * scalingFactorY;
    y2 = (selectedAreas[i].y + selectedAreas[i].height) * scalingFactorY;

    if (doTranslate) {
      y1 = doTranslateAndScale(selectedAreas[i].y, scalingFactorY);
      y2 = doTranslateAndScale((selectedAreas[i].y + selectedArea[i].height), scalingFactorY);
    }
    tArea.push([x1, y1, x2, y2].join());
  }
  return tArea;
};

const getNewColPosOffset = () => {
  let prevColPos = 0, newOffset = 0;
  const columnList = document.getElementsByClassName("draggable-column");;
  const position = $('#image-div').position();
  const divWidth = $('#image-div').width() - position.left;

  if (columnList.length) {
    prevColPos = parseInt(columnList[columnList.length-1].style.left);
  }

  if ((prevColPos + 25) > divWidth) {
    prevColPos = 0;
  }

  newOffset = prevColPos + 25;

  return newOffset;
}

const getColumnSeparators = function (selectedSeparators, scalingFactorX) {
  let colSeparators = [];

  selectedSeparators.forEach(sep => {
    colSeparators.push(sep * scalingFactorX);
  });
  colSeparators.sort(compare);

  return [colSeparators.join()];
};

const getRuleOptions = function () {
  let ruleOptions = {};
  const flavor = $('#flavors').val();
  ruleOptions['flavor'] = flavor;
  const selectedAreas = $('#image').selectAreas('areas');
  const imageWidth = $('#image').width();
  const imageHeight = $('#image').height();
  const scalingFactorX = fileDim[0] / imageWidth;
  const scalingFactorY = fileDim[1] / imageHeight;
  const hasColumnSeparator = $('.draggable-column').length > 0;

  if (selectedAreas.length > 0) {
    ruleOptions['table_area'] = getTableAreas(selectedAreas, scalingFactorX, scalingFactorY, true);
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
        let selectedSeparators = []
        $('.draggable-column').each(function (id, col) {
          selectedSeparators.push(($(col).offset().left - $(col).parent().offset().left) + ($(col).width() / 2));
        });
        ruleOptions['columns'] = getColumnSeparators(selectedSeparators, scalingFactorX);
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

const extract = function () {
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
    success: function (data) {
      const redirectUrl = '{0}//{1}/jobs/{2}'.format(window.location.protocol, window.location.host, data['job_id']);
      window.location.replace(redirectUrl);
    },
    error: function (error) {
      console.error(error);
    }
  });
}

const debugQtyAreas = function (event, id, areas) {
  return;
};

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

  $('#detect-lattice-areas').click(function () {
    areaOptions = detectTableAreas('lattice');
    $('.image-area').selectAreas('add', areaOptions);
  });

  $('#detect-stream-areas').click(function () {
    areaOptions = detectTableAreas('stream');
    $('.image-area').selectAreas('add', areaOptions);
  });

  $('.reset-areas').click(function () {
    $('.image-area').selectAreas('reset');
  });

  $('body').on('click', '.add-separator', function () {
    columnCountBuffer++;
    const position = $('#image-div').position();
    const column = $('<div id="dc" class="draggable-column"><div class="background"></div><div id="line" class="line"></div></div>');
    $(column).css({
      'top': position.top,
      'left': position.left + getNewColPosOffset(),
      'height': $('#image-div').height()
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
