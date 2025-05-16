
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Smarties‑Diabetic Companion", page_icon="💉")

st.title("Smarties‑Diabetic Companion")
st.caption("Week‑long sample data included for demo")

sample_csv = """timestamp,glucose
2025-05-12 08:00,110
2025-05-12 13:00,140
2025-05-12 20:00,180
2025-05-13 08:00,95
2025-05-13 13:00,130
2025-05-13 20:00,160
2025-05-14 08:00,105
2025-05-14 13:00,145
2025-05-14 20:00,170
2025-05-15 08:00,115
2025-05-15 13:00,135
2025-05-15 20:00,175
2025-05-16 08:00,100
2025-05-16 13:00,150
2025-05-16 20:00,165
2025-05-17 08:00,108
2025-05-17 13:00,138
2025-05-17 20:00,172
2025-05-18 08:00,112
2025-05-18 13:00,142
2025-05-18 20:00,178"""

st.download_button(
    label="Download 1‑Week Sample CSV",
    data=sample_csv,
    file_name="sample_week.csv",
    mime="text/csv"
)

uploaded = st.file_uploader("Upload your glucose CSV", type="csv")
if uploaded:
    df = pd.read_csv(uploaded)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    st.line_chart(df.set_index('timestamp')['glucose'])
