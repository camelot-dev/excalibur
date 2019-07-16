let columnCountBuffer = 0;
let globalRuleId = '';

var dgebi = document.getElementById.bind(document);
var dgebcn = document.getElementsByClassName.bind(document);
var dqs = document.querySelector.bind(document);
var dqsa = document.querySelectorAll.bind(document);

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
  let br = dgebi('image-{0}'.format(page)).getBoundingClientRect();
  const imageWidth = br.width;
  const imageHeight = br.height;
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
  let br = dgebi('image-{0}'.format(page)).getBoundingClientRect();
  const imageWidth = br.width;
  const imageHeight = br.height;
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
  const imageWidth = dgebi('image-{0}'.format(page)).getBoundingClientRect().width;
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
  const pageDiv = dgebi('image-div-{0}'.format(page));
  const br = pageDiv.getBoundingClientRect();
  const columnList = dgebcn("draggable-column");
  const divWidth = br.width - pageDiv.offsetLeft;

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
  const pageDiv = dgebi('image-div-{0}'.format(page));
  const column = document.createElement("div");
  column.className = "draggable-column";
  column.addEventListener("dblclick", onColumnSeparatorDoubleClick.bind(null, column), false);
  const columnBg = document.createElement("div");
  columnBg.className = "background";
  column.appendChild(columnBg);
  const columnLine = document.createElement("div");
  columnLine.className = "line";
  column.appendChild(columnLine);
  
  column.style.top=pageDiv.offsetTop+"px";
  column.style.left=(pageDiv.offsetLeft + colPosOffset)+"px";
  column.style.height=pageDiv.getBoundingClientRect().height+"px";
  pageDiv.appendChild(column);
  [...dgebcn("draggable-column")].forEach(e => {
    $(e).draggable({
      axis: 'x',
      containment: 'parent'
    });
  });
};

const getRuleOptions = function () {
  let ruleOptions = {'pages': {}};
  const flavor = dgebi("flavors").value;
  ruleOptions['flavor'] = flavor;

  if (flavor === null) {
    alert('Please select a Flavor from Advanced.')
  } else {
    // advanced settings
    switch(flavor.toString().toLowerCase()) {
      case 'lattice': {
        ruleOptions['process_background'] = dgebi("process-background").value ? true : false;
        ruleOptions['line_size_scaling'] = dgebi("line-size-scaling").value ? Number(dgebi("line-size-scaling").value) : 15;
        ruleOptions['split_text'] = dgebi("split-text-l").value ? true : false;
        ruleOptions['flag_size'] = dgebi("flag-size-l").value ? true : false;
        break;
      }
      case 'stream': {
        ruleOptions['row_close_tol'] = dgebi("row-close-tol").value ? Number(dgebi("line-size-scaling").value) : 2;
        ruleOptions['col_close_tol'] = dgebi("col-close-tol").value ? Number(dgebi("line-size-scaling").value) : 0;
        ruleOptions['split_text'] = dgebi("split-text-s").value ? true : false;
        ruleOptions['flag_size'] = dgebi("flag-size-s").value ? true : false;
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
    const selectedAreas = $(dgebi('image-{0}'.format(page))).selectAreas('areas');
    const hasColumnSeparator = document.querySelectorAll('#image-div-{0} > .draggable-column'.format(page)).length > 0;

    if (selectedAreas.length > 0) {
      ruleOptions['pages'][page]['table_areas'] = getTableAreasForJob(page, selectedAreas);
    } else {
      ruleOptions['pages'][page]['table_areas'] = null;
    }

    if (hasColumnSeparator) {
      let selectedSeparators = [];
      [...document.querySelectorAll('#image-div-{0} > .draggable-column'.format(page))].forEach(function (col) {
        selectedSeparators.push((col.offsetLeft - col.parentNode.offsetLeft) + (col.getBoundingClientRect().width / 2));
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
  $(dgebi('image-{0}'.format(page))).selectAreas('add', tableAreas);
};

const onDetectAreasClick = (e) => {
  resetTableAreas();
  console.log("detectedAreas", detectedAreas);
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
      let pa = detectedAreas[page];
      if(pa){
        let flName = flavor.toLowerCase();
        let paFl = pa[flName];
        if(paFl){
          renderTableAreas(page, paFl);
        }
        else{
          console.warn("no flavour", flName, "for page", page);
        }
      }
      else{
        console.warn("no detected areas for page", page);
      }
    }
  }
}

const resetTableAreas = () => {
  [...dgebcn("image-area")].forEach(e => {
    $(e).selectAreas('reset');
  });
};

// columns

const renderColumnSeparators = function(page, columnSeparators) {
  const imageWidth = dgebi('image-{0}'.format(page)).getBoundingClientRect().width;
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
    dgebcn("stream")[0].style.display="none";
    dgebcn("lattice")[0].style.display="";
    [...document.getElementsByClassName("add-separator")].forEach(e=>{e.disabled=true;});
  } else {
    dgebcn("stream")[0].style.display="";
    dgebcn("lattice")[0].style.display="none";
    [...document.getElementsByClassName("add-separator")].forEach(e=>{e.disabled=false;});
  }
};

// view and extract data

const startJob = function () {
  let ruleOptions = {};
  const loc = window.location.pathname.split('/');
  if (!globalRuleId) {
    ruleOptions = getRuleOptions();
  }
  let fd = new URLSearchParams();
  fd.append('file_id', loc[loc.length - 1]);
  fd.append('rule_id', globalRuleId);
  fd.append('rule_options', JSON.stringify(ruleOptions));
  fetch('/jobs', {
    body: fd,
    method: 'POST',
  })
  .then(function (resp) {
      let js = resp.json().then(jsr =>{
        const redirectUrl = '{0}//{1}/jobs/{2}'.format(window.location.protocol, window.location.host, jsr['job_id']);
        window.location.replace(redirectUrl);
      });
    },
    function (error) {
      console.error(error);
    }
  );
}

const debugQtyAreas = function (event, id, areas) {
  return;
};

document.addEventListener("DOMContentLoaded", function () {
  $(document.getElementsByClassName("image-area")).selectAreas({
    onChanged: debugQtyAreas
  });
}, false);
