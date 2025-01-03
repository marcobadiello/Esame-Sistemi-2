import streamlit as st

def run_readme():
    with open('README.md', 'r', encoding='utf-8') as file:
        data = file.read()
    st.markdown(data)