import streamlit as st
import pandas as pd
import psycopg2
import time
import plotly.express as px

from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=30000, key="datarefresh")

# CONNECT TO DB
conn = psycopg2.connect(
    host="dpg-d7j7a09j2pic73ai4hs0-a",
    database="mydb_anp4",
    user="mydb_anp4_user",
    password="CkaKoAx9uexixidhTUrMGWoEHVcb60hj",
    port="5432"
)

#load/query data
query = "SELECT * FROM crypto_prices ORDER BY created_at ASC"
df = pd.read_sql(query, conn)

#page title
st.title("Crypto Price Dashboard")
#show latest data
st.subheader("Latest Prices")
latest_df = df.sort_values(by='created_at').groupby("name").tail(1)
st.dataframe(latest_df, use_container_width=True)
st.caption(f"last updated at: {pd.Timestamp.now().strftime('%H:%M:%S')}")


# SELECT COINS
coins = st.multiselect(
    "Select Coins",
    df["name"].unique(),
    default=sorted(df["name"].unique()[:2])
)

if not coins:
    st.warning("Please select at least one coin")
    st.stop()

# FILTER DATA
filtered_df = df[df["name"].isin(coins)].copy()
filtered_df['created_at'] = pd.to_datetime(filtered_df['created_at'])
filtered_df = filtered_df.sort_values(by='created_at')

# METRIC (only if ONE coin)
if len(coins) == 1:
    coin = coins[0]

    coin_df = filtered_df[filtered_df["name"] == coin]

    latest = coin_df.iloc[-1]['price_usd']

    if len(coin_df) > 1:
        previous = coin_df.iloc[-2]['price_usd']
        change = latest - previous
    else:
        change = 0

    st.metric(
        label=f"{coin.upper()} Price",
        value=round(latest, 2),
        delta=round(change, 2),
        delta_color="normal" if change >= 0 else "inverse"
    )
else:
    st.info("Select one coin to see price change")

# CHART
filtered_df = filtered_df.drop_duplicates(subset='created_at')
filtered_df = filtered_df.tail(50)

fig = px.line(
    filtered_df,
    x='created_at',
    y='price_usd',
    color='name',
    title="Crypto Price Trend"
)

fig.update_layout(
    template="plotly_dark",
    xaxis_title='Time',
    yaxis_title='Price (USD)'
)

st.plotly_chart(fig, use_container_width=True)

st.caption("Data autorefreshes every 30 seconds")


