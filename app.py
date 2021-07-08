import time
import streamlit as st
import psycopg2
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import gender_guesser.detector as gender

sns.set_style('darkgrid')

st.set_page_config(layout="wide")


# Initialize connection
# Uses st.cache to only run once
@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

# App title
row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.beta_columns(
    (.1, 2.2, .2, 1, .1))
row0_1.title(':gem:TowardsDataScience Data Analysis:gem:')

with row0_2:
    st.write('')

row0_2.subheader(
    'A Web App by [Xinyi Bian:sparkles:](https://github.com/xxionias)')

# Introduction
row1_spacer1, row1_1, row1_spacer2 = st.beta_columns((.1, 3.4, .1))
with row1_1:
    st.markdown("Hey there!:wave: Welcome to Xinyi's TowardsDataScience Data Analysis \
        App. This app connectes to a Postgres database that contains data \
        [web scraped](https://github.com/xxionias/webscraping/tree/master/mediumstories) \
         from [TowardsDataScience](https:towardsdatascience.com) and analyzes data \
         about your interests from published articles, including the distribution \
         of the recommendations and responses of the articles and lengths of aricles. \
         After some nice graphs, it tries to recommend an author that contributes \
         the most to the topic that you are interested in. Give it a go!")
    st.markdown("**:leaves:To begin, please enter the key words of data science \
        topics that you are interested in (or try sample inputs!).** :point_down:")

# Data input
row2_spacer1, row2_1, row2_spacer2 = st.beta_columns((.1, 3.2, .1))
with row2_1:
    default_keyword = st.selectbox("Select one of sample keywords", (
        "Machine learning", "Statistics", "Random forest", "Clustering", "Neural Network",
        "Linear Regression", "Data Science", "Algorithms", "Python"))
    st.markdown("**or**")
    user_input = st.text_input(
        "Input your own keywords")
    if not user_input:
        user_input = default_keyword

conn.rollback()

# Perform query
# Uses st.cache to only rerun when the query changes or after 10 min
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

@st.cache
def get_data(user_input):
    sql = f"SELECT * FROM articles a LEFT JOIN users u ON a.user_id = u.user_id WHERE a.title ILIKE '%{user_input}%' ORDER BY posting_time;"
    data = run_query(sql)
    return(data)

data = get_data(user_input)

# create DataFrame using data
df = pd.DataFrame.from_records(data, columns=
    ['title', 'articleLink', 'user_id', 'posting_time', 'length_in_min', 'recommendations',
    'responses', 'user_id_d', 'author', 'authorLink', 'description', 'followers'])
df = df.drop('user_id_d', axis=1)

line1_spacer1, line1_1, line1_spacer2 = st.beta_columns((.1, 3.2, .1))

with line1_1:
    if len(df) == 0:
        st.write(f"Looks like there's no such article containing keyword '{user_input}'. Try a different keyword.")
        st.stop()

# Show progress
row3_spacer1, row3_1, row3_spacer2 = st.beta_columns((.1, 3.2, .1))
with row3_1:
    st.write(f":running:Analyzing articles that contains **{user_input}**...")

    # Add a placeholder
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
      # Update the progress bar with each iteration.
      latest_iteration.text(f'Iteration {i+1}')
      bar.progress(i + 1)
      time.sleep(0.1)

    '...and now we\'re done!'

# Display the table
row4_spacer1, row4_1, row4_spacer2 = st.beta_columns((.1, 3.2, .1))
with row4_1:
    st.subheader(f':clap:{len(df)} Articles found!(Ordered by posting time from earliest to most recent)')
    st.dataframe(df.title)


# Display Length Distribution and Recommendations Distribution
st.write('')
row5_space1, row5_1, row5_space2, row5_2, row5_space3 = st.beta_columns(
    (.1, 1, .1, 1, .1))
with row5_1:
    st.subheader(':star2:Length Distribution:star2:')
    fig = Figure()
    ax = fig.subplots()
    sns.histplot(df, x='length_in_min', color='goldenrod', ax=ax)
    ax.set_xlabel('length_in_min')
    ax.set_ylabel('Counts')
    st.pyplot(fig)

    st.markdown(":musical_note:Of all the **{}** aritcles, they require \
        **{:.2f}** min to read on average, and they most likely require **{}** \
        min to read.".format(
       len(df), df['length_in_min'].mean(), df['length_in_min'].mode()[0]
    ))

    longest = df[df.length_in_min == df.length_in_min.max()]
    if len(longest) == 1:
        st.markdown(":musical_note:The longest article is **[{}]({})**. It requires \
            **{}** min to read. The article is written by user **[{}]({})** who has \
            **{}** followers!".format(
            longest.iloc[0].title, longest.iloc[0].articleLink, longest.iloc[0].length_in_min,
            longest.iloc[0].author, longest.iloc[0].authorLink, longest.iloc[0].followers
        ))
        # Add description if exists
        if longest.iloc[0].description != 'NaN':
            st.markdown(":musical_note:His/Her/Their description is **{}**".format(
                longest.iloc[0].description
            ))
    else:
        st.markdown(":musical_note:The longest articles require **{}** min to read.".format(
            longest.iloc[0].length_in_min
        ))

with row5_2:
    st.subheader(':star2:Recommendations Distribution:star2:')
    fig = Figure()
    ax = fig.subplots()
    sns.histplot(df, x='recommendations', color='cornflowerblue', ax=ax)
    ax.set_xlabel('Recommendations')
    ax.set_ylabel('Counts')
    st.pyplot(fig)

    st.markdown(":musical_note:Of all the **{}** aritcles, they receive **{:.0f}** \
        recommendations on average, and they most likely receive **{}** recommendations.".format(
        len(df), int(df['recommendations'].mean()), df['recommendations'].mode()[0]
    ))

    recommendations = df[df.recommendations == df.recommendations.max()]
    if len(recommendations) == 1:
        st.markdown(":musical_note:The most popular article titled **[{}]({})** \
            receives **{}** recommendations! The article is written by \
            user **[{}]({})** who has **{}** followers!".format(
           recommendations.iloc[0].title, recommendations.iloc[0].articleLink,
           recommendations.iloc[0].recommendations, recommendations.iloc[0].author,
           recommendations.iloc[0].authorLink, recommendations.iloc[0].followers
        ))
        # Add description if exists
        if recommendations.iloc[0].description != 'NaN':
            st.markdown(":musical_note:His/Her/Their description is **{}**".format(
                recommendations.iloc[0].description
            ))
    else:
        st.markdown(":musical_note:The most popular articles receive **{}** recommendations.".format(
            recommendations.iloc[0].recommendations
        ))

# Display Responses Distribution and Followers Distribution
st.write('')
row6_space1, row6_1, row6_space2, row6_2, row6_space3 = st.beta_columns(
    (.1, 1, .1, 1, .1))
with row6_1:
    st.subheader(':star2:Responses Distribution:star2:')
    fig = Figure()
    ax = fig.subplots()
    sns.histplot(df, x='responses', color='goldenrod', ax=ax)
    ax.set_xlabel('Responses')
    ax.set_ylabel('Counts')
    st.pyplot(fig)

    st.markdown(":musical_note:Of all the **{}** aritcles, they receive \
        **{:.2f}** responses on average, and they most likely receive **{}** \
        responses".format(
        len(df), df.responses.mean(), df.responses.mode()[0]
    ))

    responses = df[df.responses == df.responses.max()]
    if responses.iloc[0].responses != 0:
        if len(responses) == 1:
            st.markdown(":musical_note:The most popular article titled **[{}]({})** \
                receives **{}** responses! The article is written by user **[{}]({})** \
                who has **{}** followers!".format(
               responses.iloc[0].title, responses.iloc[0].articleLink,
               responses.iloc[0].responses, responses.iloc[0].author,
               responses.iloc[0].authorLink, responses.iloc[0].followers
            ))
            # Add description if exists
            if responses.iloc[0].description != 'NaN':
                st.markdown(":musical_note:His/Her/Their description is **{}**".format(
                    responses.iloc[0].description
                ))
        else:
            st.markdown(":musical_note:The most popular articles receive **{}** responses.".format(
                responses.iloc[0].responses
            ))
with row6_2:
    users = df.drop_duplicates(subset=['user_id'], keep='last')

    st.subheader(':star2:Followers Distribution:star2:')
    fig = Figure()
    ax = fig.subplots()
    sns.histplot(df, x='followers', color='cornflowerblue', ax=ax)
    ax.set_xlabel('Followers')
    ax.set_ylabel('Counts')
    st.pyplot(fig)

    st.markdown(":musical_note:**{}** authors contribute to **{}** aritcles, they \
        have **{:.2f}** followers on average, and they most likely have **{}** \
        followers.".format(
        len(users), len(df), users.followers.mean(), users.followers.mode()[0]
    ))

    followers = users[users.followers == users.followers.max()]
    if followers.iloc[0].followers != 0:
        if len(followers) == 1:
            st.markdown(":musical_note:The author **[{}]({})** is the most popular \
                author with **{}** followers!".format(
                followers.iloc[0].author, followers.iloc[0].authorLink,
                followers.iloc[0].followers
            ))
            # Add description if exists
            if followers.iloc[0].description != 'NaN':
                st.markdown(":musical_note:His/Her/Their description is **{}**".format(
                    followers.iloc[0].description
                ))
        else:
            st.markdown(":musical_note:The most popular authors have **{}** followers.".format(
                followers.iloc[0].followers
            ))

st.write('')
row7_space1, row7_1, row7_space2, row7_2, row7_space3 = st.beta_columns((.1, 1, .1, 1, .1))
with row7_1:
    st.subheader(":star2:Followers vs. Recommendations:star2:")
    fig = Figure()
    ax = fig.subplots()
    sns.scatterplot(data=df, x='followers', y='recommendations', color='cornflowerblue', ax=ax)
    ax.set_xlabel('Followers')
    ax.set_ylabel('Recommendations')
    st.pyplot(fig)

    st.markdown(":musical_note:The scatterplot plots the relationship between author's followers and articles' recommendations.")

with row7_2:
    st.subheader(":star2:Posting Time vs. Recommendations:star2:")
    fig = Figure()
    ax = fig.subplots()
    sns.scatterplot(data=df, x='posting_time', y='recommendations', color='cornflowerblue', ax=ax)
    ax.set_xlabel('Posting Time')
    # plt.xticks(rotation = 45)
    # ax.set_xticklabels(ax.get_xticks(), rotation = 45)
    ax.tick_params(axis='x', labelrotation = 45)
    ax.set_ylabel('Recommendations')
    st.pyplot(fig)

    st.markdown(":musical_note:The scatterplot plots the relationship between articles' posting times and articles' recommendations.")


# Summary
st.write('')
row8_spacer1, row8_1, row8_spacer2 = st.beta_columns((.1, 3.4, .1))
with row8_1:
    st.header(':sparkling_heart:Who is the most prolific author under the topic **{}**?:sparkling_heart:'.format(user_input))

    user_counts_df = df.groupby(['user_id', 'author']).size().reset_index(name='counts').sort_values(by="counts", ascending=False)

    # st.dataframe(user_counts_df)
    if len(user_counts_df) <= 1:
        st.markdown(":exclamation:It seems like there aren't enough data existed to \
            provide information. Try another keyword!")

    elif (user_counts_df['counts'].iloc[0] == user_counts_df['counts'].iloc[1]) and (user_counts_df['counts'].iloc[1] != user_counts_df['counts'].iloc[2]):
        st.markdown(":musical_note:The most prolific users under this topic are **[{}]({})** and **[{}]({})** \
            who each wrote **{}** articles to the topic".format(
                user_counts_df['author'].iloc[0], df[df['author'] == user_counts_df['author'].iloc[0]].authorLink.iloc[0],
                user_counts_df['author'].iloc[1], df[df['author'] == user_counts_df['author'].iloc[1]].authorLink.iloc[0],
                user_counts_df['counts'].iloc[0]
            ))
    elif user_counts_df['counts'].iloc[0] != user_counts_df['counts'].iloc[1]:
        st.markdown(":musical_note:The most prolific user under this topic is **[{}]({})** \
            who wrote **{}** articles to the topic".format(
                user_counts_df['author'].iloc[0], df[df['author'] == user_counts_df['author'].iloc[0]].authorLink.iloc[0],
                user_counts_df['counts'].iloc[0]
            ))
    else:
        st.markdown(":exclamation:There are more than 2 authors contribute the most \
            to this topic. Try another keyword!")
