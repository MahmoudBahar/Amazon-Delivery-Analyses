import streamlit as st
import pandas as pd
import requests
from io import BytesIO

st.set_page_config(layout="wide", initial_sidebar_state='collapsed')
@st.cache_data
def load_data():
    return pd.read_pickle(BytesIO(requests.get("https://github.com/MahmoudBahar/Amazon-Delivery-Analyses/raw/main/Amazon%20Delivery%20Dataset/amazon_delivery_cleaned_and_extracted_features_final_streamlit.pkl").content))
if 'df' not in st.session_state:
    st.session_state.df = load_data()
    st.session_state.load_data = load_data

pg = st.navigation([st.Page("./pages/overview_page.py",
                            title="Overview",
                            icon=":material/overview:",
                            default=True
                           ),
                    st.Page("./pages/analysis_page.py",
                            title="Analysis",
                            icon=":material/analytics:",
                            default=False
                           ),
                    st.Page("./pages/map_page.py",
                            title="Map Analysis",
                            icon=":material/map:",
                            default=False
                           ),
                    st.Page("./pages/agent_page.py",
                            title="Agent Analysis",
                            icon=":material/person:",
                            default=False
                           )])
pg.run()
