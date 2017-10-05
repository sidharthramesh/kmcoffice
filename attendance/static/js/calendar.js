var CalendarJs = (function () {

  'use strict';

  function InvalidMonthError(message) {
    this.message = message;
    this.name = 'InvalidMonthError';
  };
  function InvalidMonthsAbbrError(message) {
    this.message = message;
    this.name = 'InvalidMonthsAbbrError';
  };
  function InvalidMonthsError(message) {
   this.message = message;
   this.name = 'InvalidMonthsError';
  };

  var MONTHS = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
  ];

  var WEEKDAYS = [
    'Sunday',
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
  ];

  function generateMonthsAbbr(months) {
    return months.map(function(month) {
      return month.slice(0, 3);
    });
  }

  return (function(config) {
    var _months = MONTHS;
    var _monthsAbbr = generateMonthsAbbr(MONTHS);

    if (config && config.months) {
      if (! Array.isArray(config.months)) {
        throw new InvalidMonthsError('Months array must have 12 values');
      }

      if (config.months.length !== 12) {
        throw new InvalidMonthsError('Months array must have 12 values');
      }

      _months = config.months;
      _monthsAbbr = generateMonthsAbbr(config.months);
    }

    if (config && config.monthsAbbr) {
      if (! Array.isArray(config.monthsAbbr)) {
        throw new InvalidMonthsAbbrError('Months array must have 12 values');
      }

      if (config.monthsAbbr.length !== 12) {
        throw new InvalidMonthsAbbrError('Months array must have 12 values');
      }

      _monthsAbbr = config.monthsAbbr;
    }

    return {
      months: function() {
        return _months;
      },

      monthsAbbr: function() {
        return _monthsAbbr;
      },

      years: function(from, to) {
        if (from > to) {
          throw new RangeError('The first year argument cannot be greater than the second');
        }

        var years = [ from.toString() ];
        var totalYears = to - from + 1;

        while (years.length < totalYears) {
          var year = parseInt(years[years.length - 1], 10) + 1;

          years.push(year.toString());
        }

        return years;
      },

      yearsAbbr: function(from, to) {
        var years = this.years(from, to).map(function(year) {
          return year.toString().substring(2);
        });

        return (years.length > 1)
          ? years
          : years[0];
      },

      weekdays: function() {
        return WEEKDAYS;
      },

      weekdaysAbbr: function() {
        return this.weekdays().map(function(weekday) {
          return weekday.slice(0, 3);
        });
      },

      generateCalendar: function(numberOfDays, firstWeekday, lastWeekday) {
        var lastDay = 0;
        firstWeekday--;
        if (firstWeekday < 0) firstWeekday = 6;

        var flag = true;
        var init = true;
        var day = 0;
        var calendar = [];
        while (day < numberOfDays) {
          var week = [];
          for (var i = 0; i < 7; i++) {
            if (day < numberOfDays) {
              if (init) {
                if (i === firstWeekday) {
                  week.push(++day);
                  init = false;
                }
                else {
                  week.push(0);
                }
              }
              else {
                week.push(++day);
              }
            }
            else {
              week.push(0);
            }
          }
          calendar.push(week);
        }

console.log(calendar);
        return calendar;
      },

      of: function(year, month, transformer) {
        if (month < 0 || month > 11) {
          throw new InvalidMonthError('Month should be beetwen 0 and 11');
        }

        if (typeof year !== 'number' || typeof month !== 'number') {
          throw new Error('Arguments should be numbers');
        }

        var numberOfDays =  new Date(year, month + 1, 0).getDate();
        var firstWeekday = new Date(year, month, 1).getDay();
        var lastWeekday = new Date(year, month, numberOfDays).getDay();

        const data = {
          year: year.toString(),
          yearAbbr: this.yearsAbbr(year),
          month: this.months()[month],
          monthAbbr: this.monthsAbbr()[month],
          weekdays: this.weekdays(),
          weekdaysAbbr: this.weekdaysAbbr(),
          days: numberOfDays,
          firstWeekday: firstWeekday,
          lastWeekday: lastWeekday,
          calendar: this.generateCalendar(numberOfDays, firstWeekday, lastWeekday),
        };

        if (typeof transformer === 'function') {
          return transformer(data);
        }

        return data;
      },
    };
  })();
})();
