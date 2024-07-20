import streamlit as st
import plotly.express as px
from st_aggrid import AgGrid
import requests
# with open('./animations/analysis-animate.svg', 'r') as file:
#     svg_content = file.read()
@st.cache_data
def load_svg():
    return requests.get("https://raw.githubusercontent.com/MahmoudBahar/Amazon-Delivery-Analyses/main/StreamLit/animations/analysis-animate.svg").content.decode('utf-8')
st.markdown(f"<div style='width: 300px; height: 300px; align: center'>{load_svg()}</div>", unsafe_allow_html=True)
st.title("Detailed Analysis")
tab1, tab2 = st.tabs(['Static Analysis', 'Dynamic Analysis'])
with tab1:
    st.header("Vehicles Along Pick-up Time")
    fig = px.line(st.session_state.df.groupby(['Pickup Time', 'Vehicle']).agg('count')['Agent Age'].rename('count').reset_index(['Vehicle']).sort_index(), y='count', color='Vehicle', template='plotly_dark', color_discrete_sequence=px.colors.qualitative.Dark24).update_layout(yaxis_title='Number of orders')
    st.plotly_chart(fig)
    
    st.header("Store Types And Delivery Categories And Drop Types")
    fig = px.treemap(st.session_state.df, path=['Store Type Of Location', 'Category', 'Drop Type Of Location'], template='plotly_dark', height=700, color_discrete_sequence=px.colors.qualitative.Bold)
    st.plotly_chart(fig)

    choice = st.radio('Location:', options=('Store', 'Drop'), index = 0, help='Choose the location of the store or drop', horizontal=True)
    st.header(f"{choice} Locations")
    fig = px.sunburst(st.session_state.df, path=[f'{choice} Country', f'{choice} State', f'{choice} City District'], template = 'plotly_dark', height=700, color_discrete_sequence=px.colors.qualitative.Dark24 if choice == 'Store' else px.colors.qualitative.Dark24_r)
    st.plotly_chart(fig)
    
with tab2:
    def fig1():
        if 'x' not in st.session_state:
            st.session_state.x = st.session_state.x_old = st.session_state.y = st.session_state.y_old = None
            st.session_state.c = st.session_state.c_old = st.session_state.s = st.session_state.s_old = None
            st.session_state.f = st.session_state.f_old = None
            st.session_state.bar = st.session_state.bar_old = 'relative'
        def histo():
            st.plotly_chart(px.histogram(data_frame=st.session_state.df.astype('string'), x=st.session_state.x, y=st.session_state.y, color=st.session_state.c, pattern_shape=st.session_state.s, histfunc=st.session_state.f, barmode=st.session_state.bar, color_discrete_sequence=px.colors.qualitative.Dark24))
            
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.session_state.x = st.selectbox(label='x-axis', options=[None] + list(st.session_state.df.columns[1:]), index=0, key = 11)
        with col2:
            st.session_state.y = st.selectbox(label='y-axis', options=[None] + list(st.session_state.df.columns), index=0, key = 12)
        with col3:
            st.session_state.c = st.selectbox(label='color', options=[None] + list(st.session_state.df.select_dtypes('string').columns[1:]), index=0, key = 13)
        with col4:
            st.session_state.s = st.selectbox(label='shape', options=[None] + list(st.session_state.df.select_dtypes('string').columns[1:]), index=0, key = 14)
        with col5:
            st.session_state.f = st.selectbox(label='function', options=[None , 'count', 'sum', 'avg', 'min', 'max'], index=0, key = 15)
        st.session_state.bar = st.radio('Barmode', options=('relative', 'group', 'overlay'), index = 0, horizontal = True)
        
        if st.session_state.x != st.session_state.x_old or st.session_state.y != st.session_state.y_old or st.session_state.c != st.session_state.c_old or st.session_state.s != st.session_state.s_old or st.session_state.f != st.session_state.f_old or st.session_state.bar != st.session_state.bar_old:
            if st.session_state.y is not None or st.session_state.x is not None:
                histo()
            st.session_state.x_old = st.session_state.x
            st.session_state.y_old = st.session_state.y
            st.session_state.c_old = st.session_state.c
            st.session_state.s_old = st.session_state.s
            st.session_state.bar_old = st.session_state.bar
    def fig2():
        st.header("Filter by Vehicle Type")
        vehicle_type = st.selectbox("Select Vehicle Type", st.session_state.df['Vehicle'].unique())
        filtered_data = st.session_state.df[st.session_state.df['Vehicle'] == vehicle_type]
        AgGrid(filtered_data)
    fig1()
    fig2()
