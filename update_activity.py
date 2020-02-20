import csv
import itertools
import getpass
import json
import os
from argparse import ArgumentParser
from datetime import datetime

import requests

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S-08:00"


def retrieve_token(email, password):
    token = None
    for _ in range(3):
        print("Trying to retrieve access token. Attempt {}".format(_ + 1))
        if all([email, password]):
            json_data = json.dumps({"email": email, "password": password, "remember_me": True})
        else:
            raise AttributeError("Username or password not provided")
        response = requests.post('https://tracker-api.toptal.com/sessions', headers=headers, data=json_data)
        token = response.json().get("access_token")
        if token:
            return token

    raise Exception("Token not retrieved")


headers = {
    'authority': 'tracker-api.toptal.com',
    'accept': 'application/json, text/plain, */*',
    'origin': 'https://tracker.toptal.com',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'content-type': 'application/json;charset=UTF-8',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'referer': 'https://tracker.toptal.com/signin?return-to=/app/my-activities',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
}


def read_records_from_csv(csv_file_name):
    if not os.path.exists(csv_file_name):
        raise FileNotFoundError("File {} doesn't exist".format(csv_file_name))
    rows = []
    with open(csv_file_name) as file:
        n = 38
        reader = csv.DictReader(itertools.islice(file, n, None))
        keys = ["date", "project name", "description", "start time", "end time", "projectId"]
        for row in reader:
            item = {}
            should_add_item = True
            for k in keys:
                value = row[k]
                if not value:
                    should_add_item = False
                    break
                item[k] = value
            if should_add_item:
                rows.append(item)

    return rows


def date_formatter(date, start_time, end_time):
    date_vals = date.split("-")
    if len(start_time) < 5:
        start_time = "0" + start_time
    if len(end_time) < 5:
        end_time = "0" + end_time
    formatted_date = "-".join([date_vals[-1], date_vals[0], date_vals[1]])  # YYYY-mm-dd
    if len(date_vals[0]) == 4:
        formatted_date = date # already in YYYY-mm-dd
    timezone_offset = get_timezone_offset_from_date(formatted_date)
    start_date = formatted_date + "T" + start_time + timezone_offset
    end_date = formatted_date + "T" + end_time + timezone_offset
    return start_date, end_date

def get_timezone_offset_from_date(date):
    string_tz_offset = datetime.fromisoformat(date).astimezone().strftime("%z")
    return ":00{}:{}".format(string_tz_offset[:-2], string_tz_offset[-2:])

if __name__ == "__main__":
    parser = ArgumentParser()
    optional = parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    required.add_argument("-e", "--email", type=str, help="Your toptracker email [endswith @bitquilltech.com].", required=True)
    required.add_argument("-f", "--file", type=str, help="Your timekeeping template file (csv).", required=True)
    optional.add_argument("-p", "--password", type=str, help="Your toptracker password.", required=False)
    parser._action_groups.append(optional)

    args = parser.parse_args()
    email = args.email
    file = args.file
    if args.password is None:
        password = getpass.getpass()
    else:
        password = args.password
    
    rows = read_records_from_csv(file)
    items = []
    for row in rows:
        date, start_time, end_time, description, projectId = row["date"], row["start time"], row["end time"], row["description"], row["projectId"]
        start, end = date_formatter(date, start_time, end_time)
        items.append((start, end, description, projectId))

    access_token = retrieve_token(email, password)
    json_payloads = []

    for item in items:
        payload = dict()
        payload["description"] = item[2].rstrip()
        payload["start_time"] = item[0].rstrip()
        payload["end_time"] = item[1].rstrip()
        payload["projectId"] = item[3].rstrip()
        payload["user_agent"] = {
                "client": "Web",
                "os_type": "mac",
                "browser_type": "chrome"
        }
        payload["access_token"] = access_token
        json_payloads.append(payload)

    for i, payload in enumerate(json_payloads):
        print("Item: {}, Description: {}, start_time: {}, end_time: {}, Project Id: {}".format(
            i+1, payload["description"], payload["start_time"], payload["end_time"], payload["projectId"]))
        projectId = payload["projectId"]
        response = requests.post('https://tracker-api.toptal.com/projects/{}/activities'.format(projectId), headers=headers,data=json.dumps(payload))
        if(response.status_code == 201):
            print("SUCCESS: Response Code: {}".format(response.status_code))
        else:
            print("ERROR: Response Code: {}, Respone Content:{}".format(response.status_code, response.content))
