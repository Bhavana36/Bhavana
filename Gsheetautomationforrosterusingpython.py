# importing the necessary libraries that are required to run the automation
import requests
import json
import schedule
import gspread
import pandas as pd
from datetime import date
import time
from tabulate import tabulate

# Function starts from here
def automation():

    # getting the current date and replacing the 0 for the first 10 numbers and removing the year
    today = date.today()
    d = today.strftime('%d-%b').replace(' 0', ' ')
    # This JSON file helps in connecting the Gsheet to this code.
    cred_file = "sample.json"
    gc = gspread.service_account(cred_file)
    database = gc.open("gsheet name")
    list_wks = database.worksheet("worksheet name")
    # Converting the data from the sheet to Pandas Dataframe
    data = pd.DataFrame(list_wks.get_all_records())
    df1 = data['MEMBERS'][0:15]
    df2 = data.loc[0:14, d]
    frames = [df1, df2]
    df = pd.concat(frames, axis=1)
    # Fetching the records based on our requirements and merging the data columns
    df5 = df[df[d].str.contains("H")]
    df6 = df[df[d].str.contains("PL")]
    df3 = df[df[d].str.contains("WO")]
    df4 = df[df[d].str.contains("UPL")]
    df7 = df[df[d].str.contains("CO")]
    frames1 = [df3, df4, df5, df6, df7]
    dfnew = pd.concat(frames1, axis=0)
    # Converting the data frame data into table format(there are different formats)
    f = tabulate(dfnew, headers=["column 1", "column 2", "column 3"], tablefmt="presto")
    print(f)
    # Based on the data availability we are sending the gsheet data to slack using the slack API
    if dfnew.empty:
        empty_payload = {"channel": "channel id",  "text": "sample text", "attachments": [
            {
                "text": "attachment text",
                "color": "#3AA3E3",
                "attachment_type": "default"

            }
        ]}

        HEADERS = {
           'Authorization': "slack App token",
           'Content-Type': "application/json"
        }
        Url = 'https://slack.com/api/chat.postMessage'
        empty_response = requests.request("POST", Url, json=empty_payload, headers=HEADERS)
        print(empty_response)
    else:
         payload = {"channel": "channel id",  "text": "sample text", "attachments": [
                {
                    "text": "attachment text",
                    "color": "#3AA3E3",
                    "attachment_type": "default"

                }
             ]}
         HEADERS = {
           'Authorization': "slack App token",
           'Content-Type': "application/json"
         }
         Url = 'https://slack.com/api/chat.postMessage'
         response = requests.request("POST", Url, json=payload, headers=HEADERS)
         print(response)


automation()
# Running the scheduler for every 10 mins
schedule.every(10).minutes.do(automation)
while True:
    schedule.run_pending()
    time.sleep(5)
