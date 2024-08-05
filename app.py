# app.py

import streamlit as st
from logics.example_logics import get_greeting, summarize_text

st.title('LLM Web Application game')

if st.button('Greet'):
    greeting = get_greeting()
    st.write(greeting)

text_to_summarize = st.text_area("Enter text to summarize")
if st.button('Summarize'):
    summary = summarize_text(text_to_summarize)
    st.write(summary)

