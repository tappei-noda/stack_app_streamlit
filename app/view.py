import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import time
import yfinance as yf
import altair as alt
st.title("株価可視化アプリ")
tickers = {
    "biprogy":"8056.T",
    "amazon":"AMZN",
    "google":"GOOGL",
    "netflix":"NFLX",
}
st.sidebar.write("""
# 日経株価
株価可視化ツールです。以下のオプションから表示日数を指定して下さい
""")

st.sidebar.write("""
表示日表示
""")

days = st.sidebar.slider('日数',1,50,20)

st.sidebar.write("""
株価の範囲の指定
""")

try:
    stock_range_min,stock_range_max = st.sidebar.slider('範囲を指定してください',0.00,3500.00,(0.00,3500.00))

    st.write(f"過去{days}日の株価です")
    @st.cache
    def get_data(days,tickers):
        """_summary_

        Args:
            days (_type_): 表示日数
            tickers (_type_): 株価コードの種類

        Returns:
            _type_: 結合されたデータフレーム
        """
        df = pd.DataFrame()
        for company in tickers.keys():
            tkr = yf.Ticker(tickers[company])
            hist = tkr.history(periof=f'{days}d')
            hist.index = hist.index.strftime("%d %B %Y")
            hist = hist[['Close']]
            hist.columns = [company]
            hist = hist.T
            hist.index.name = 'Name'
            df = pd.concat([df,hist])
        return df

    df = get_data(days,tickers)
    companies = st.multiselect(
        "会社を選択してください",
        list(df.index),
        default = ["biprogy","google"],
    )
    if not companies:
        st.error("少なくとも一つの会社を選んでください")
    else:
        data = df.loc[companies]
        st.write("### 株価 ###",data.sort_index())

    data = data.T.reset_index()
    data = pd.melt(data,id_vars=['Date']).rename(columns={'value':'Stock Prices(USD)'})
    chart = (
        alt.Chart(data)
        .mark_line(opacity=0.8,clip=True)
        .encode(
            x="Date:T",
            y=alt.Y("Stock Prices:Q",stack=None,scale=alt.Scale(domain=[stock_range_min,stock_range_max])),
            color='Name:N'
        )
    )
    st.altair_chart(chart,use_container_width=True)
except:
    st.error(
        "error is corror"
    )