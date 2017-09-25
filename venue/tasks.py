from celery import shared_task, task
import requests, datetime
from django.core.mail import send_mail as mail
import json
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build
@task
def insert_event(name,location,descripion,start,end,calId='mpo2f09j62aolu1jlgd7r0c89k@group.calendar.google.com'):
    scopes = ['https://www.googleapis.com/auth/calendar']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'account.json', scopes,
    )
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    event = {
    'summary': name,
    'location': location,
    'description': descripion,
    'start': {
        'dateTime': start,
    },
    'end': {
        'dateTime': end,
    },
    'reminders': {
        'useDefault': False,
        'overrides': [
        {'method': 'popup', 'minutes': 10},
        ],
    },
    }
    event = service.events().insert(calendarId=calId, body=event).execute()
    return event