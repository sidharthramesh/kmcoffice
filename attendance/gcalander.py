from datetime import datetime, timedelta
from dateutil import parser
from pytz import timezone
import requests
from decouple import config
from .models import Department

key = config('CAL_KEY')


def get_classes(date_string, batch):
  url = "https://www.googleapis.com/calendar/v3/calendars/{calander_id}/events".format(calander_id=batch.calander_id)
  india = timezone('Asia/Calcutta')
  start = parser.parse(date_string).replace(tzinfo=india)
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
  print(a.status_code)
  print(s)
  classes = []
  for c in s['items']:
    des = c.get('description')
    if not des is None:

      dept = Department.objects.get(name=c.get('description')).pk
    else:
      
      dept = None
      for dep in Department.objects.all():
        #print("Did not get desc. Searching {} in {}".format(c.get('summary'), dep))
        if dep.name in c.get('summary'):
          #print("Found")
          dept = dep.pk
          break
    
      
    period = {
      'start':c['start']['dateTime'],
      'end':c['end']['dateTime'],
      'department':dept,
      'name':c.get('summary'),
      'location':c.get('location'),
      'batch': batch.pk,
    }
    classes.append(period)
  return classes