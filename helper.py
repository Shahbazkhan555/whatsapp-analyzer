from wordcloud import WordCloud
import pandas as pd
from collections import Counter


def fetch_stats(selected_user, df):

    if selected_user != "Overall":
        df = df[df["users"] == selected_user]

    # fetching total messages
    num_messages = df.shape[0]
    # fetching total words
    words = []
    for message in df["messages"]:
        words.extend(message.split())

    return num_messages, len(words),


def most_busy_users(df):
    # barplot of 5 most busy person in the chat
    x = df["users"].value_counts().head(5)
    # dataframe of most busy persons in %
    new_df = round((df["users"].value_counts()/df.shape[0])*100, 2).reset_index().rename(columns={"index":"Name", "users":"Percentage"})

    return x, new_df


def create_word_cloud(selected_user,df):
    f = open("stop_hinglish.txt", 'r')
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df["users"] == selected_user]

    def remove_stop_words(message):
        words = []
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
        return "".join(word)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df["messages"] = df["messages"].apply(remove_stop_words)
    df_wc = wc.generate(df["messages"].str.cat(sep=" "))

    return df_wc


def most_common_words(selected_user,df):

    f = open("stop_hinglish.txt", 'r')
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df["users"] == selected_user]

    words = []
    for message in df["messages"]:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))[2:]

    return most_common_df


def monthly_timeline(selected_user, df):

    if selected_user != "Overall":
        df = df[df["users"] == selected_user]

    timeline = df.groupby(["year", "month", "month_num"], sort=False).count()["messages"].reset_index()

    month_date = []
    for i in range(timeline.shape[0]):
        month_date.append(timeline["month"][i] + "-" + str(timeline["year"][i]))

    timeline["monthyear"] = month_date

    return timeline

def daily_timeline(selected_user, df):

    if selected_user != "Overall":
        df = df[df["users"] == selected_user]

    daily_timeline = df.groupby(["only_date"], sort=False).count()["messages"].reset_index()

    return daily_timeline

def week_activity_map(selected_user, df):

    if selected_user != "Overall":
        df = df[df["users"] == selected_user]

    return df["day_name"].value_counts()


def month_activity_map(selected_user, df):

    if selected_user != "Overall":
        df = df[df["users"] == selected_user]

    return df["month"].value_counts()


def activity_heatmap(selected_user, df):

    if selected_user != "Overall":
        df = df[df["users"] == selected_user]

    user_heatmap = df.pivot_table(index="day_name", columns="period", values="messages", aggfunc="count").fillna(0)

    return user_heatmap