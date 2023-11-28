import streamlit as st
import clickhouse_connect

# st.set_page_config(layout="wide")
left_col, right_col = st.columns(2)
with left_col:
    st.image(
            "https://images.ctfassets.net/paqvtpyf8rwu/GeLUVavqqxhFZolzU9jM3/3b8dddc74a632e63f17e0a5e40b971bb/super-panda-update.svg",
            width=250,
    )
with right_col:
    st.title("Redpanda Demo")


st.write("Demonstration of a live video game leaderboard built with Redpanda, ClickHouse, and Streamlit.")
st.divider()

# Connect to ClickHouse
client = clickhouse_connect.get_client(
    host = "localhost",
    port = 18123,
    username = "default",
    password = ""
)


# Calculate the metrics
st.subheader("Overview")

# How many unique players are streaming in their scores?
query = """
select count(distinct(player)) as unique_players
from foo.scores_view
limit 1
"""
df_unique = client.query_df(query)

# How many players are active during the last minute?
query = """
select count(player) as unique_players_1min 
from foo.scores_view
where created_at >= DATE_SUB(now(), INTERVAL 1 MINUTE )
limit 1
"""
df_unique_1min = client.query_df(query)

metric1, metric2 = st.columns(2)
metric1.metric(
    label="Total players",
    value=df_unique['unique_players'].values[0]
)
metric2.metric(
    label="Active in last minute",
    value=df_unique_1min['unique_players_1min'].values[0]
)


# Formulate the query for the leaderboard
query = """
select player, sum(score) as total
from foo.scores_view as sv
group by player
order by total desc
limit 10
"""

# Run the query and get the results as a Pandas dataframe
df = client.query_df(query)

# Display the dataframe as an HTML table
st.subheader("Leaderboard")
st.dataframe(
    df,
    hide_index=True,
    use_container_width=True
)