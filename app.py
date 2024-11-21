import streamlit as st
from Estrattore import df
import Tools

st.title("Spotify wrapped statistico")
st.write(df)
Tools.banner_canzone_small("7x8dCjCr0x6x2lXKujYD34")
Tools.banner_canzone_big("7x8dCjCr0x6x2lXKujYD34")


# Sidebar con emoji
st.sidebar.title("Menù")
scelta = st.sidebar.radio("🌟 Scegli un'opzione:", ["🚀 Opzione 1", "🌈 Opzione 2", "🧩 Opzione 3"])
