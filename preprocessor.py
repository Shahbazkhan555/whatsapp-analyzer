import re
import pandas as pd


def preprocess(data):
    pattern = '\[\d{1,2}\/\d{2,4}\/\d{2,4},\s\d{1,2}:\d{1,2}:\d{1,2}]\s'
    messages = re.split(pattern, data)[1:]

    pattern2 = '\[\d{1,2}\/\d{2,4}\/\d{2,4},\s\d{1,2}:\d{1,2}:\d{1,2}]'
    dates = re.findall(pattern2, data)
    dates_without_brac = []
    for i in dates:
        i = i.replace('[', '').replace(']', '')
        dates_without_brac.append(i)

    df = pd.DataFrame({'user_message': messages, 'date': dates_without_brac})
    df['date'] = pd.to_datetime(df["date"], format='%d/%m/%y, %H:%M:%S')

    messages = []
    users = []
    for msg in df["user_message"]:
        entry = re.split('^(.+?):', msg)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append("group notification")
            messages.append(entry[0])

    df["users"] = users
    df["messages"] = messages

    df.drop(columns=["user_message"], inplace=True)

    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month_name()
    df["day"] = df["date"].dt.day
    df["hour"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute

