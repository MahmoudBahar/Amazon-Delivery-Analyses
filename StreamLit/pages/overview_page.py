import streamlit as st
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid
import requests


palette = [
    "#323434", "#E1BCDA", "#8A8783", "#EADE61", "#F1EBE0", "#424445",
    "#B9B4A7", "#C8D0D2", "#E5C1B1", "#A6B7B9", "#F4A8A1", "#9B9B9B", "#D6E0C4","#F9F5E5"]

# with open('./animations/delivery-animate.svg', 'r') as file:
#     svg_content = file.read()
st.markdown(f"<div style='width: 300px; height: 300px; align: center'>{requests.get("https://github.com/MahmoudBahar/Amazon-Delivery-Analyses/blob/main/StreamLit/animations/analysis-animate.svg").content}</div>", unsafe_allow_html=True)
st.title("Delivery Data Overview")

st.header("Summary Statistics")
st.write(st.session_state.df.describe())
st.write(st.session_state.df.select_dtypes('string').describe())

st.header("Order Count by Category")
fig = px.bar(st.session_state.df['Category'].value_counts().reset_index(), x='Category', y='count', color='Category', labels={'count': 'Number of orders'}, color_discrete_sequence=px.colors.qualitative.Pastel).update_layout(showlegend=False)
st.plotly_chart(fig)
    
st.sidebar.title("Settings")
if st.sidebar.checkbox("Show raw data"):
    st.subheader("Raw Data")
    if 'ID' not in locals():
        ID = ''
        password = ''
        edit = False
    if not edit:
        ID = st.text_input("", placeholder="Order ID", max_chars=13, autocomplete='off', value=ID)
    col1, col2 = st.columns([1,1])
    with col1:
        edit = st.checkbox("Edit raw data")
    if edit:
        st.warning("You are about to edit the raw data!")
        password = st.text_input("", placeholder="password", autocomplete='password', value = password, type='password')
        if password == '12345678':
            with col2:
                reset = st.button("Reset Data")
            if reset:
                st.session_state.df = pd.read_pickle(BytesIO(requests.get("https://github.com/MahmoudBahar/Amazon-Delivery-Analyses/raw/main/Amazon%20Delivery%20Dataset/amazon_delivery_cleaned_and_extracted_features_final_streamlit.pkl").content))
                st.success("Data reseted successfully!", icon = '✅')
            st.session_state.df = st.data_editor(st.session_state.df)
        elif password != '':
            st.error("Wrong password!")
    else:
        st.dataframe((st.session_state.df.loc[ID] if ID in st.session_state.df.index else {f"{ID}": 'not found'}) if ID != '' else st.session_state.df, hide_index=True if ID == '' else False)
