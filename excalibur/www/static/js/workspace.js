let columnCountBuffer = 0;
let globalRuleId = '';

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

const getTableAreasForRender = function (page, detectedAreas) {
  const imageWidth = $('#image-{0}'.format(page)).width();
  const imageHeight = $('#image-{0}'.format(page)).height();
  const scalingFactorX = imageWidth / fileDims[page][0];
  const scalingFactorY = imageHeight / fileDims[page][1];

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

const getTableAreasForJob = function (page, selectedAreas) {
  const imageWidth = $('#image-{0}'.format(page)).width();
  const imageHeight = $('#image-{0}'.format(page)).height();
  const scalingFactorX = fileDims[page][0] / imageWidth;
  const scalingFactorY = fileDims[page][1] / imageHeight;

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

const getColumnSeparators = function (page, selectedSeparators) {
  const imageWidth = $('#image-{0}'.format(page)).width();
  const scalingFactorX = fileDims[page][0] / imageWidth;

  let colSeparators = [];

  selectedSeparators.forEach(sep => {
    colSeparators.push(sep * scalingFactorX);
  });
  colSeparators.sort(compare);

  return [colSeparators.join()];
};

const onSavedRuleClick = function (e) {
  const rule_id = e.getAttribute('data-rule-id');
  globalRuleId = rule_id;
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

        console.log(ruleOptions);
        if (Object.keys(ruleOptions['pages']).length) {
          resetTableAreas();
          resetColumnSeparators();
          for (let page in ruleOptions['pages']) {
            if ('table_areas' in ruleOptions['pages'][page]) {
              let tableAreas = [];
              const table_areas = ruleOptions['pages'][page]['table_areas'];
              table_areas.forEach(function (t) {
                tableAreas.push(t.split(',').map(Number));
              })
              renderTableAreas(page, tableAreas);
            }
            if ('columns' in ruleOptions['pages'][page]) {
              let columnSeparators = [];
              const columns = ruleOptions['pages'][page]['columns'];
              columns.forEach(function (c) {
                columnSeparators.push(c.split(',').map(Number));
              })
              renderColumnSeparators(page, columnSeparators);
            }
          }
        }

        if (ruleOptions['flavor'].toLowerCase() == 'lattice') {
          document.getElementById('process-background').value = ruleOptions['process_background'];
          document.getElementById('line-size-scaling').value = ruleOptions['line_size_scaling'];
          document.getElementById('split-text-l').value = ruleOptions['split_text'];
          document.getElementById('flag-size-l').value = ruleOptions['flag_size'];
        } else if (ruleOptions['flavor'].toLowerCase() == 'stream') {
          document.getElementById('row-close-tol').value = ruleOptions['row_close_tol'];
          document.getElementById('col-close-tol').value = ruleOptions['col_close_tol'];
          document.getElementById('split-text-s').value = ruleOptions['split_text'];
          document.getElementById('flag-size-s').value = ruleOptions['flag_size'];
        } else {
          console.log('Unknown flavor {0}'.format(ruleOptions['flavor']));
        }
      }
    },
    error: function (error) {
    }
  });
};

const getNewColPosOffset = function (page) {
  let prevColPos = 0, newOffset = 0;
  const pageDiv = '#image-div-{0}'.format(page);
  const columnList = document.getElementsByClassName("draggable-column");
  const position = $(pageDiv).position();
  const divWidth = $(pageDiv).width() - position.left;

  if (columnList.length) {
    prevColPos = parseInt(columnList[columnList.length-1].style.left);
  }

  if ((prevColPos + 25) > divWidth) {
    prevColPos = 0;
  }

  newOffset = prevColPos + 25;

  return newOffset;
}

const addColumnSeparator = function (page, colPosOffset) {
  const pageDiv = '#image-div-{0}'.format(page);
  const position = $(pageDiv).position();
  const column = $('<div id="dc" class="draggable-column" ondblclick="onColumnSeparatorDoubleClick(this)"><div class="background"></div><div id="line" class="line"></div></div>');
  $(column).css({
    'top': position.top,
    'left': position.left + colPosOffset,
    'height': $(pageDiv).height()
  });
  $(pageDiv).append(column);
  $('.draggable-column').draggable({
    axis: 'x',
    containment: 'parent'
  });
};

const getRuleOptions = function () {
  let ruleOptions = {'pages': {}};
  const flavor = $('#flavors').val();
  ruleOptions['flavor'] = flavor;

  if (flavor === null) {
    alert('Please select a Flavor from Advanced.')
  } else {
    // advanced settings
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
        break;
      }
      default: {
        break;
      }
    }
  }

  // table areas and columns for each page
  for (let page in detectedAreas) {
    ruleOptions['pages'][page] = {};
    const selectedAreas = $('#image-{0}'.format(page)).selectAreas('areas');
    const hasColumnSeparator = $('#image-div-{0} > .draggable-column'.format(page)).length > 0;

    if (selectedAreas.length > 0) {
      ruleOptions['pages'][page]['table_areas'] = getTableAreasForJob(page, selectedAreas);
    } else {
      ruleOptions['pages'][page]['table_areas'] = null;
    }

    if (hasColumnSeparator) {
      let selectedSeparators = []
      $('#image-div-{0} > .draggable-column'.format(page)).each(function (id, col) {
        selectedSeparators.push(($(col).offset().left - $(col).parent().offset().left) + ($(col).width() / 2));
      });
      ruleOptions['pages'][page]['columns'] = getColumnSeparators(page, selectedSeparators);
    } else {
      ruleOptions['pages'][page]['columns'] = null;
    }
  }

  return ruleOptions;
};

// onevent functions
// table areas

const renderTableAreas = function (page, tableAreas) {
  tableAreas = getTableAreasForRender(page, tableAreas);
  $('#image-{0}'.format(page)).selectAreas('add', tableAreas);
};

const onDetectAreasClick = (e) => {
  resetTableAreas();
  let flavor = document.getElementById('flavors').value;
  if (flavor == 'Select flavor') {
    for (let page in detectedAreas) {
      let f = '';
      if (detectedAreas[page]['lattice'] != null) {
        f = 'lattice';
      } else {
        f = 'stream';
      }
      renderTableAreas(page, detectedAreas[page][f]);
      onFlavorChange();
      document.getElementById('flavors').value = f.charAt(0).toUpperCase() + f.slice(1);
    }
  } else {
    for (let page in detectedAreas) {
      renderTableAreas(page, detectedAreas[page][flavor.toLowerCase()]);
    }
  }
}

const resetTableAreas = () => {
  $('.image-area').each(function () {
    $(this).selectAreas('reset');
  });
};

// columns

const renderColumnSeparators = function(page, columnSeparators) {
  const imageWidth = $('#image-{0}'.format(page)).width();
  const scalingFactorX = imageWidth / fileDims[page][0];

  for (let i = 0; i < columnSeparators.length; i++) {
    addColumnSeparator(page, columnSeparators[i] * scalingFactorX);
  }
};

const onAddSeparatorClick = (e) => {
  columnCountBuffer++;
  const page = e.getAttribute('data-page');
  const colPosOffset = getNewColPosOffset(page);
  addColumnSeparator(page, colPosOffset);
}

const onColumnSeparatorDoubleClick = (e) => {
  e.parentNode.removeChild(e);
}

const resetColumnSeparators = function () {
  const columnSeparatorsCollection = document.getElementsByClassName('draggable-column');
  const columnSeparators = Array.from(columnSeparatorsCollection);
  columnSeparators.forEach(function (e) {
    e.parentNode.removeChild(e);
  });
};

// flavor select

const onFlavorChange = function () {
  const flavor = document.getElementById('flavors').value;
  if (flavor == 'Lattice') {
    $('.stream').hide();
    $('.lattice').show();
    $('.add-separator').prop('disabled', true);
  } else {
    $('.stream').show();
    $('.lattice').hide();
    $('.add-separator').prop('disabled', false);
  }
};

// view and extract data

const startJob = function () {
  let ruleOptions = {};
  const loc = window.location.pathname.split('/');
  if (!globalRuleId) {
    ruleOptions = getRuleOptions();
  }
  $.ajax({
    url: '/jobs',
    data: {
      file_id: loc[loc.length - 1],
      rule_id: globalRuleId,
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
