from datetime import datetime, timedelta
from pytz import timezone
import requests
from decouple import config
calander_id = 'pi2m3dda6ljkrmh473624vvl9s@group.calendar.google.com'
key = config('CAL_KEY')
url = "https://www.googleapis.com/calendar/v3/calendars/{calander_id}/events".format(calander_id=calander_id)

def get_classes(year,month,date):
  india = timezone('Asia/Calcutta')
  start = datetime(year,month,date,tzinfo=india)
  end = start + timedelta(days=1)
  a = requests.get(url,
  {
    'key':key,
    'orderBy':'startTime',
    'singleEvents':True,
    'timeMax': end.isoformat('T'),
    'timeMin': start.isoformat('T'),
    })

  s = a.json()
  classes = []
  for c in s['items']:
    period = {
      'start':c['start']['dateTime'],
      'end':c['end']['dateTime'],
      'department':c.get('description'),
      'name':c.get('summary'),
      'location':c.get('location'),
    }
    classes.append(period)
  return classes