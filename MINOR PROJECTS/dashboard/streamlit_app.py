from __future__ import annotations

import pandas as pd
import requests
import streamlit as st

try:
    API_URL = st.secrets.get('API_URL', 'http://localhost:8000')
except Exception:
    API_URL = 'http://localhost:8000'
API_URL = API_URL.rstrip('/')

st.set_page_config(page_title='AI Stock Recommendation Dashboard', layout='wide')

st.title('AI-Powered Stock Market Recommendation Dashboard')
st.caption('Educational and research use only. Not financial advice.')

symbols = ['AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN']
selected_symbol = st.selectbox('Select stock symbol', symbols)

try:
    response = requests.get(f'{API_URL}/api/stocks/{selected_symbol}/analysis', timeout=20)
    response.raise_for_status()
    result = response.json()
except requests.RequestException as exc:
    st.error(f'Could not load analysis from the backend at {API_URL}.')
    st.caption(f'Check that the API is running and API_URL is configured correctly. Details: {exc}')
    st.stop()

col1, col2, col3, col4 = st.columns(4)
col1.metric('Price', f"${result.get('price', 0):,.2f}")
col2.metric('Recommendation', result.get('recommendation', 'HOLD'))
col3.metric('Confidence', f"{result.get('confidence', 0) * 100:.0f}%")
col4.metric('Final Score', f"{result.get('final_score', 0):.2f}")

st.subheader('Summary')
st.write(result.get('reason', 'No reason provided.'))

with st.expander('Technical indicators'):
    st.json(result.get('technical_summary', {}))

st.subheader('Performance Snapshot')
chart_data = pd.DataFrame(
    {
        'close': [98, 100, 99, 101, 103, 102, 104, 106, 108, 110],
        'sma_20': [95, 96, 96.5, 97, 98, 99, 100, 101, 102, 103],
        'sma_50': [90, 91, 92, 94, 95, 95.5, 96, 97, 98, 99],
    }
)
st.line_chart(chart_data)

st.subheader('Recent Financial News')
for article in result.get('news', [])[:3]:
    st.markdown(f"**{article.get('headline', 'News')}**")
    st.write(article.get('summary', ''))
    st.caption(f"{article.get('source', 'Unknown')} • {article.get('published_at', '')}")

st.warning('Educational and research use only. This project is not financial advice.')
