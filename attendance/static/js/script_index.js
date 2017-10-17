let eventActivator = false;

// Batches
var Batches = (function () {
  var callback = function (batch) {
    Classes.renderListing();
  }; // CALLBACK FOR CLICKS
  var batchstand = document.getElementById('batch_batches');
  batchstand.innerHTML = Object.keys(batches).map(function (value) {
    return '<div data-value="' + value + '">' + batches[value] + '</div>';
  }).join('');
  var currSelection = batchstand.querySelector('div[data-value]');
  currSelection.className = "selected";
  if (eventActivator) {
    callback(currSelection.getAttribute('data-value'));
  }
  batchstand.querySelectorAll('div[data-value]').forEach(function (ele) {
    ele.addEventListener('click', function () {
      if (currSelection) {
        currSelection.className = "";
      }
      currSelection = this;
      currSelection.className = "selected";
      if (eventActivator) {
        callback(currSelection.getAttribute('data-value'));
      }
    }, false);
  });
  return function () {
    return currSelection.getAttribute('data-value');
  }
})();

// Calendar
var Calendar = (function () {
  var Cal = function () {
    this.month = document.getElementById('classes_calendar_month');
    this.nextMonth = document.getElementById('classes_calendar_next');
    this.body = document.getElementById('classes_calendar_dates');
    this.callback = function (date) {
      Classes.renderListing();
    }; // CALLBACKS FOR CLICKS

    this.curr = {
      moment: moment(),
      ele: {}
    };

    document.getElementById('classes_calendar_prev').addEventListener('click', function () {
      this.curr.moment = this.curr.moment.month(this.curr.moment.month() - 1);
      this.curr.moment = this.curr.moment.date(1);
      this.setToCurr();
    }.bind(this), false);
    document.getElementById('classes_calendar_next').addEventListener('click', function () {
      this.curr.moment = this.curr.moment.month(this.curr.moment.month() + 1);
      this.curr.moment = this.curr.moment.date(1);
      this.setToCurr();
    }.bind(this), false);

    this.setToCurr();

    return this;
  };
  Cal.prototype = {
    setToCurr: function () {
      this.setToMonthAndYear(this.curr.moment.month(), this.curr.moment.year());
      this.selectDate(this.curr.moment.format("YYYY-MM-DD"));
    },
    setToMonthAndYear: function (month, year) {
      var data = CalendarJs.of(year, month);
      this.month.innerHTML = data.month + " " + data.year;
      var data_cal = data.calendar;
      this.body.innerHTML = data_cal.map(function (row) {
        return "<tr>" + row.map(function (cell) {
          if (cell > 0) {
            return '<td data-value="' + year + '-' + ((month + 1) < 10 ? "0" + (month + 1) : (month + 1)) +  '-' + (cell < 10 ? "0" + cell : cell) + '">' + cell + '</td>';
          }
          else {
            return "<td></td>";
          }
        }).join('') + "</tr>";
      }).join('');
      var parent = this;
      this.body.querySelectorAll('td[data-value]').forEach(function (ele) {
        ele.addEventListener('click', function (e) {
          this.curr.moment.date(parseInt(e.target.getAttribute('data-value').split('-')[2]));
          this.selectDate(e.target.getAttribute('data-value'));
        }.bind(parent), false);
      });
    },
    selectDate: function (date) {
      if (this.curr.ele) {
        this.curr.ele.className = "";
      }
      this.curr.ele = this.body.querySelector('td[data-value="' + date + '"]');
      this.curr.ele.className = "selected";
      if (eventActivator) {
        this.callback(date);
      }
    }
  };
  var calen = new Cal();
  return function () {
    return calen.curr.moment;
  };
})();

// Class Listing
var Classes = (function () {
  // vars
  var ele = document.getElementById('classes_datedList');
  var currentClasses = [];
  var currBatch = "";
  var currDate = "";
  function renderDept () {
    return `<select>` + Object.keys(departments).map(function (key) {
      return `<option value="` + key + `">` + departments[key] + `</option>`;
    }).join('') + `</select>`;
  };
  function renderListing () {
    // get date
    var date = Calendar();
    date = date.format("YYYY-M-D");
    // get batches
    var batch = Batches();
    // show loading
    ele.innerHTML = `<div class="tooltip" style="text-align:center;">Loading...</div>`;
    // check if to use cache or not
    if (date === currDate && batch === currBatch) {
      console.log("FROM CACHE");
      setCurrentClasses(currentClasses);
    }
    else {
      // get request
      var xmlhttp;
      if (window.XMLHttpRequest) {
        xhttp = new XMLHttpRequest();
      } else {
        xhttp = new ActiveXObject("Microsoft.XMLHTTP");
      }
      xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          // respond to get
          var classList = JSON.parse(this.responseText);
          currentClasses = classList.classes;
          setCurrentClasses(classList);
        }
        else if (this.readyState == 4 && this.stats != 200) {
          ele.innerHTML = `<div class="tooltip" style="text-align:center;">An Error Occured...</div>`;
        }
      };
      xhttp.open("GET", "/attendance/class_data?date=" + date + "&batch=" + batch, true);
      xhttp.send();
      currDate = date;
      currBatch = batch;
    }
  };
  function createClassCard (class_, index) {
    var el = document.createElement('div');
    el.innerHTML = `<div><h2>CLASS_NAME</h2><p>START_TIME - END_TIME</p><span>DATE</span><div>DEPT</div><div class="validation"></div></div><div class="click"><img src="/static/checkbox-unchecked.png"/><input type="hidden"/></div>`
      .replace('CLASS_NAME', class_.name)
      .replace('START_TIME', moment(class_.start).format('h:mm a'))
      .replace('END_TIME', moment(class_.end).format('h:mm a'))
      .replace('DATE', moment(class_.start).format('dddd, Do MMMM'))
      .replace('DEPT', (class_.department !== null ? departments[class_.department] : renderDept()));
    el.setAttribute('data-index', index);
    el.querySelector('.click').addEventListener('click', function () {
      var i = parseInt(this.parentNode.getAttribute('data-index'));
      Selected.addToList(i, currentClasses[i].department === null ? this.parentNode.querySelector('select').value : null);
      this.parentNode.parentNode.removeChild(this.parentNode);
    }, false);
    return el;
  };
  function setCurrentClasses () {
    ele.innerHTML = "";
    if (currentClasses.length > 0) {
      for (var i = 0; i < currentClasses.length; i++) {
        // remove all selected classes from here
        if (Selected.indexOf(currentClasses[i]) === -1) {
          ele.appendChild(createClassCard(currentClasses[i], i));
        }
      }
    }
    else {
      ele.innerHTML = `<div class="tooltip" style="text-align:center;">There Are No Classes On This Day...</div>`;
    }
  };
  return {
    renderListing: renderListing,
    getCurrentClass: function (index) {
      return JSON.parse(JSON.stringify(currentClasses[index]));
    }
  };
})();

// Selected Classes
var Selected = (function () {
  var list  = [];
  var ele = document.getElementById('classes_selection_selection');
  function indexOf (item) {
    var flag = true;
    list.forEach(function (i, index) {
      if (i) {
        if (i.start === item.start) {
          console.log("CLASH ", index);
          flag = index;
        }
      }
    });
    if (flag === true) {
      return -1;
    }
    else {
      return flag;
    }
  };
  function createClaimCard (class_, index) {
    var el = document.createElement('div');
    el.innerHTML = `<div><h2>CLASS_NAME</h2><p>START_TIME - END_TIME</p><span>DATE</span><div>DEPT</div><div class="validation"></div></div><div class="click"><img src="/static/checkbox-checked.png"/><input type="hidden"/></div>`
      .replace('CLASS_NAME', class_.name)
      .replace('START_TIME', moment(class_.start).format('h:mm a'))
      .replace('END_TIME', moment(class_.end).format('h:mm a'))
      .replace('DATE', moment(class_.start).format('dddd, Do MMMM'))
      .replace('DEPT', departments[class_.department]);
    el.setAttribute('data-index', index)
    el.querySelector('.click').addEventListener('click', function () {
      var i = parseInt(this.parentNode.getAttribute('data-index'));
      removeFromList(i);
      this.parentNode.parentNode.removeChild(this.parentNode);
    }, false);
    return el;
  };
  function renderSelectedList () {
    if (list.length > 0) {
      ele.innerHTML = "";
      list.forEach(function (i, index) {
        if (i) {
          ele.appendChild(createClaimCard(i, index));
        }
      });
    }
    else {
      ele.innerHTML = `<div class="tooltip" style="text-align:center;">Add the classes you missed.</div>`;
    }
  };
  function removeFromList (index) {
    list[index] = undefined;
    Classes.renderListing();
  };
  function addToList (index, selectedDept) {
    // TODO Sort
    var data = Classes.getCurrentClass(index);
    data.department = selectedDept ? selectedDept : data.department;
    if (indexOf(data) === -1) {
      list.push(data);
      renderSelectedList();
    }
  }
  function getList () {
    return list;
  }
  renderSelectedList();
  return {
    addToList: addToList,
    indexOf: indexOf,
    getList: getList
  }
})();

// Events
var Events = (function () {
  var callback = function (event_) {
    console.log(event_);
  };
  var eventstand = document.getElementById('events_stand');
  eventstand.innerHTML = Object.keys(events).map(function (value) {
    return '<option value="' + value + '">' + events[value] + '</option>';
  }).join('');
  var currEvent = eventstand.value;
  if (eventActivator) {
    callback(events[currEvent])
  }
  function setCurrEvent (val) {
    currEvent = val;
  }
  eventstand.addEventListener('change', function () {
    setCurrEvent(this.value);
  }, false);
  return function () {
    return currEvent;
  }
})();

// Startup
(function () {
  window.addEventListener('load', function () {
    Classes.renderListing();
    eventActivator = true;
  }, false);
})();
