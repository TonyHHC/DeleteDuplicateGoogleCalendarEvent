from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.events', 'https://www.googleapis.com/auth/calendar']


def main():
	creds = None
	# The file token.json stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	
	if os.path.exists('token.json'):
		creds = Credentials.from_authorized_user_file('token.json', SCOPES)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open('token.json', 'w') as token:
			token.write(creds.to_json())

	try:
	
		service = build('calendar', 'v3', credentials=creds)

		# Call the Calendar API
		now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
		print('List all events')
	
		# List Calendars
		'''
		page_token = None
		while True:
			calendar_list = service.calendarList().list(pageToken=page_token).execute()
			for calendar_list_entry in calendar_list['items']:
				print(calendar_list_entry['id'], '>>>>>', calendar_list_entry['timeZone'], '>>>>>', calendar_list_entry['summary'])
			page_token = calendar_list.get('nextPageToken')
			if not page_token:
				break
		'''
	
		duplicate_event_id = []
		# List Duplicate Events
		page_token = None
		while True:
			events = service.events().list(calendarId='abc@gmail.com', pageToken=page_token, maxResults=25000, orderBy='startTime', singleEvents=True).execute()
			old_startdate = ''
			old_summary = ''
			for event in events['items']:
				start = event.get('start')
				startdate = 'none'
				if 'dateTime' in start:
					startdate = start['dateTime'][:10]
				if 'date' in start:
					startdate = start['date']
					
				if startdate == old_startdate and event.get('summary') == old_summary:
					print(startdate, '>>>', event['id'], '>>>', event.get('summary'))
					duplicate_event_id.append( event['id'])
						
				old_startdate = startdate
				old_summary = event.get('summary')
					
					
			page_token = events.get('nextPageToken')
			if not page_token:
				break
				
		# Delete duplicate event
		print('-----------------')
		for event_id in duplicate_event_id:
			print('Delete ', event_id)
			service.events().delete(calendarId='abc@gmail.com', eventId=event_id).execute()

	except HttpError as error:
		print('An error occurred: %s' % error)


if __name__ == '__main__':
	main()