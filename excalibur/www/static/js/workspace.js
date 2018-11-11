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

const getTableAreasForRender = function (detectedAreas) {
  const imageWidth = $('#image').width();
  const imageHeight = $('#image').height();
  const scalingFactorX = imageWidth / fileDim[0];
  const scalingFactorY = imageHeight / fileDim[1];

  let tableAreas = [];
  let x1, x2, y1, y2;
  for (let i = 0; i < detectedAreas.length; i++) {
    x1 = detectedAreas[i][0] * scalingFactorX;
    x2 = detectedAreas[i][2] * scalingFactorX;
    y1 = (detectedAreas[i][1]) * scalingFactorY;
    y2 = (detectedAreas[i][3]) * scalingFactorY;
    const tableArea = {
      x: Math.floor(x1),
      y: Math.floor(Math.abs(y1 - imageHeight)),
      width: Math.floor(Math.abs(x2 - x1)),
      height: Math.floor(Math.abs(y2 - y1))
    };
    tableAreas.push(tableArea);
  }
  return tableAreas;
};

const renderTableAreas = function (tableAreas) {
  tableAreas = getTableAreasForRender(tableAreas);
  $('.image-area').selectAreas('add', tableAreas);
};

const getTableAreasForJob = function (selectedAreas) {
  const imageWidth = $('#image').width();
  const imageHeight = $('#image').height();
  const scalingFactorX = fileDim[0] / imageWidth;
  const scalingFactorY = fileDim[1] / imageHeight;

  let tableAreas = [];
  let x1, x2, y1, y2;
  for (let i = 0; i < selectedAreas.length; i++) {
    x1 = selectedAreas[i].x * scalingFactorX;
    x2 = (selectedAreas[i].x + selectedAreas[i].width) * scalingFactorX;
    y1 = Math.abs(selectedAreas[i].y - imageHeight) * scalingFactorY;
    y2 = Math.abs(selectedAreas[i].y + selectedAreas[i].height - imageHeight) * scalingFactorY;
    tableAreas.push([x1, y1, x2, y2].join());
  }
  return tableAreas;
};

const getNewColPosOffset = function () {
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

const addColumnSeparator = function (colPosOffset) {
  const position = $('#image-div').position();
  const column = $('<div id="dc" class="draggable-column" ondblclick="onColumnSeparatorDoubleClick(this)"><div class="background"></div><div id="line" class="line"></div></div>');
  $(column).css({
    'top': position.top,
    'left': position.left + colPosOffset,
    'height': $('#image-div').height()
  });
  $('#image-div').append(column);
  $('.draggable-column').draggable({
    axis: 'x',
    containment: 'parent'
  });
};

const renderColumnSeparators = function(columnSeparators) {
  const imageWidth = $('#image').width();
  const scalingFactorX = imageWidth / fileDim[0];

  for (let i = 0; i < columnSeparators.length; i++) {
    addColumnSeparator(columnSeparators[i] * scalingFactorX);
  }
};

const getColumnSeparators = function (selectedSeparators) {
  const imageWidth = $('#image').width();
  const scalingFactorX = fileDim[0] / imageWidth;

  let colSeparators = [];

  selectedSeparators.forEach(sep => {
    colSeparators.push(sep * scalingFactorX);
  });
  colSeparators.sort(compare);

  return [colSeparators.join()];
};

const onFlavorChange = function () {
  const flavor = document.getElementById('flavors').value;
  if (flavor == 'Lattice') {
    $('.stream').hide();
    $('.lattice').show();
  } else {
    $('.stream').show();
    $('.lattice').hide();
  }
};

const onSavedRuleChange = function () {
  const rule_id = document.getElementById('rules').value;
  $.ajax({
      url: '/rules/{0}'.format(rule_id),
      type: 'GET',
      success: function (data) {
        if (data['message'] == 'Rule not found') {
          console.log(data['message']);
        } else {
          const ruleOptions = data['rule_options'];
          onFlavorChange();
          document.getElementById('flavors').value = ruleOptions['flavor'];
          if (ruleOptions['flavor'].toLowerCase() == 'lattice') {
            let tableAreas = [];
            const table_areas = ruleOptions['table_areas'];
            table_areas.forEach(function (t) {
              tableAreas.push(t.split(',').map(Number));
            })

            resetTableAreas();
            renderTableAreas(tableAreas);

            document.getElementById('process-background').value = ruleOptions['process_background'];
            document.getElementById('line-size-scaling').value = ruleOptions['line_size_scaling'];
            document.getElementById('split-text-l').value = ruleOptions['split_text'];
            document.getElementById('flag_size-l').value = ruleOptions['flag_size'];
          } else if (ruleOptions['flavor'].toLowerCase() == 'stream') {
            let tableAreas = [];
            const table_areas = ruleOptions['table_areas'];
            table_areas.forEach(function (t) {
              tableAreas.push(t.split(',').map(Number));
            })

            resetTableAreas();
            renderTableAreas(tableAreas);

            let columnSeparators = [];
            const columns = ruleOptions['columns'];
            columns.forEach(function (c) {
              columnSeparators.push(c.split(',').map(Number));
            })

            resetColumnSeparators();
            renderColumnSeparators(columnSeparators);

            document.getElementById('row-close-tol').value = ruleOptions['row_close_tol'];
            document.getElementById('col_close_tol').value = ruleOptions['col_close_tol'];
            document.getElementById('split-text-s').value = ruleOptions['split_text'];
            document.getElementById('flag_size-s').value = ruleOptions['flag_size'];
          } else {
            console.log('Unknown flavor {0}'.format(ruleOptions['flavor']));
          }
        }
      },
      error: function (error) {
      }
    });
};

const resetTableAreas = () => {
  $('.image-area').selectAreas('reset');
};

const resetColumnSeparators = function () {
  const columnSeparatorsCollection = document.getElementsByClassName('draggable-column');
  const columnSeparators = Array.from(columnSeparatorsCollection);
  columnSeparators.forEach(function (e) {
    e.parentNode.removeChild(e);
  });
};

const onDetectAreasClick = (e) => {
  const flavor = e.getAttribute('data-flavor');
  renderTableAreas(detectedAreas[flavor]);
}

const onAddSeparatorClick = (e) => {
  columnCountBuffer++;
  const colPosOffset = getNewColPosOffset();
  addColumnSeparator(colPosOffset);
}

const onColumnSeparatorDoubleClick = (e) => {
  e.parentNode.removeChild(e);
}

const getRuleOptions = function () {
  let ruleOptions = {};
  const flavor = $('#flavors').val();
  const selectedAreas = $('#image').selectAreas('areas');
  const hasColumnSeparator = $('.draggable-column').length > 0;

  ruleOptions['flavor'] = flavor;

  if (selectedAreas.length > 0) {
    ruleOptions['table_areas'] = getTableAreasForJob(selectedAreas);
  } else {
    ruleOptions['table_areas'] = null;
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
        ruleOptions['columns'] = getColumnSeparators(selectedSeparators);
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

const startJob = function () {
  let ruleOptions = {};
  const loc = window.location.pathname.split('/');
  const rule_id = document.getElementById('rules').value;
  if (!rule_id) {
    ruleOptions = getRuleOptions();
  }
  $.ajax({
    url: '/jobs',
    data: {
      file_id: loc[loc.length - 1],
      rule_id: rule_id,
      page_numbers: $('#page-numbers').val() ? $('#page-numbers').val() : '1',
      rule_options: JSON.stringify(ruleOptions)
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
});
