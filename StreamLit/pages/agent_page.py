import streamlit as st
import plotly.express as px

with open('./animations/delivery-animate2.svg', 'r') as file:
    svg_content = file.read()
st.markdown(f"<div style='width: 300px; height: 300px; align: center'>{svg_content}</div>", unsafe_allow_html=True)
st.title("Agent Performance")

st.header("Agent Rating Distribution")
fig = px.histogram(st.session_state.df.astype('string'), x=st.session_state.df['Agent Rating'].astype('string'))
st.plotly_chart(fig)

st.header("Agent Age Distribution")
fig = px.histogram(st.session_state.df.astype('string'), x='Agent Age')
st.plotly_chart(fig)

st.header("Filter by Agent Rating")
rating = st.slider("Select Rating", min_value=0.0, max_value=5.0, value=(0.0, 5.0))
filtered_data = st.session_state.df[(st.session_state.df['Agent Rating'] >= rating[0]) & (st.session_state.df['Agent Rating'] <= rating[1])]
st.write(filtered_data)
