"""Simple sliding window dashboard-style
plot that updates periodically pulling from
a random generator
"""
import streamlit as st
import time
import random

# values cannot be used in st.session_state!!
if 'my_values' not in st.session_state:
    st.session_state.my_values = list()

if not st.session_state.my_values:
  st.session_state.my_values.append(0)

st.line_chart(st.session_state.my_values[-100:])

new_value = st.session_state.my_values[-1] + random.randrange(-100, 100) / 100

st.session_state.my_values.append(new_value)

time.sleep(.2)

st.experimental_rerun()