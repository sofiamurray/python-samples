# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START drive_activity_quickstart]
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/activity'


def main():
    """Runs the sample.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('appsactivity', 'v1', http=creds.authorize(Http()))

    # Call the Drive Activity API
    results = service.activities().list(source='drive.google.com',
                                        drive_ancestorId='root',
                                        pageSize=10).execute()
    activities = results.get('activities', [])
    if not activities:
        print('No activity.')
    else:
        print('Recent activity:')
        for activity in activities:
            event = activity['combinedEvent']
            user = event.get('user', None)
            target = event.get('target', None)
            if user is None or target is None:
                continue
            time = datetime.datetime.fromtimestamp(
                int(event['eventTimeMillis'])/1000)
            print(u'{0}: {1}, {2}, {3} ({4})'.format(time,
                                                     user['name'],
                                                     event['primaryEventType'],
                                                     target['name'],
                                                     target['mimeType']))


if __name__ == '__main__':
    main()
# [END drive_activity_quickstart]
