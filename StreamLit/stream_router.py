import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
@st.cache_data
def load_data():
    st.session_state.df = pd.read_pickle('./amazon_delivery_cleaned_and_extracted_features_final_streamlit.pkl')
if 'df' not in st.session_state:
    load_data()
    st.session_state.reset_data = load_data

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