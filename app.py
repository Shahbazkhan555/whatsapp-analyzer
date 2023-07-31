import streamlit as st
import re
import pandas as pd
import helper
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor


st.sidebar.title("WhatsApp Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")


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
    df["month_num"] = df["date"].dt.month
    df["only_date"] = df["date"].dt.date
    df["day"] = df["date"].dt.day
    df["day_name"] = df["date"].dt.day_name()
    df["hour"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute

    period = []
    for hour in df[["day_name", "hour"]]["hour"]:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df["period"] = period

    st.dataframe(df)

    # fetch unique users
    user_list = df['users'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        # Stats Area
        num_messages, words = helper.fetch_stats(selected_user,df)

        col1, col2 = st.columns(2)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        # message flow monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['monthyear'], timeline['messages'], color="green")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # message flow daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['messages'], color="black")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # acitivity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            # weekly activity
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        with col2:
            # monthly activity
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color="orange")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        # displaying heatmap of weekly activity of users in every hour
        st.title("Weekly Activity Map")
        user_activity = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_activity)
        st.pyplot(fig)


        # Buisiest persons
        if selected_user == "Overall":
            st.title("Most Busy Users")
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color="red")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # creating wordcloud
        st.title("WordCloud")
        df_wc = helper.create_word_cloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        #most common words
        most_common_df = helper.most_common_words(selected_user,df)

        fig, ax = plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1])

        st.title("Most Common Words")
        st.pyplot(fig)

