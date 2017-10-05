// Batches
var Batches = (function () {
  var batchstand = document.getElementById('batch_batches');
  batchstand.innerHTML = Object.keys(batches).map(function (value) {
    return '<div data-value="' + value + '">' + batches[value] + '</div>';
  }).join('');
  var currSelection = batchstand.querySelector('div[data-value]');
  currSelection.className = "selected";
  batchstand.querySelectorAll('div[data-value]').forEach(function (ele) {
    ele.addEventListener('click', function () {
      if (currSelection) {
        currSelection.className = "";
      }
      currSelection = this;
      currSelection.className = "selected";
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
      console.log(date);
    };

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
      console.log(data);
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
          console.log(moment(e.target.getAttribute('data-value')));
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
      this.callback(date);
    }
  };
  var calen = new Cal();
  return function () {
    return calen.curr.moment;
  };
})();

// Class Listing
function renderListing (batch, date) {
  if (!batch || !date) {
    return false;
  }
};

// Other

// Selected Classes

// Events
