import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from st_aggrid import AgGrid
import streamlit.components.v1 as components
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

st.set_page_config(page_title='Analyses', page_icon='🚚', initial_sidebar_state='collapsed')

palette = [
    "#323434", "#E1BCDA", "#8A8783", "#EADE61", "#F1EBE0", "#424445",
    "#B9B4A7", "#C8D0D2", "#E5C1B1", "#A6B7B9", "#F4A8A1", "#9B9B9B", "#D6E0C4","#F9F5E5"]

@st.cache_data
def load_data():
    return pd.read_pickle('../Amazon Delivery Dataset/amazon_delivery_cleaned_and_extracted_features_final_kepler.pkl')

df = load_data()

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Detailed Analysis", "Maps", "Agent Performance"])

if page == "Overview":
    with open('./animations/delivery-animate.svg', 'r') as file:
        svg_content = file.read()
    st.markdown(f"<div style='width: 300px; height: 300px; align: center'>{svg_content}</div>", unsafe_allow_html=True)
    st.title("Delivery Data Overview")

    st.header("Summary Statistics")
    st.write(df.describe())
    
    st.header("Order Count by Category")
    fig = px.bar(df['Category'].value_counts().reset_index(), x='Category', y='Category', labels={'index': '', 'Category': 'Number of orders'}, color_discrete_sequence=['maroon'])
    st.plotly_chart(fig)
    

elif page == "Detailed Analysis":
    with open('./animations/analysis-animate.svg', 'r') as file:
        svg_content = file.read()
    st.markdown(f"<div style='width: 300px; height: 300px; align: center'>{svg_content}</div>", unsafe_allow_html=True)
    st.title("Detailed Analysis")
    tab1, tab2 = st.tabs(['Static Analysis', 'Dynamic Analysis'])
    with tab1:
        st.header("Traffic Along Pick-up Time")
        fig = px.line(df.pivot_table(values='Traffic', index='Pickup Time', aggfunc='count').sort_index(), y='Traffic', template='plotly_dark', color_discrete_sequence=['maroon'])
        st.plotly_chart(fig)
        
        st.header("Store Types And Delivery Categories And Drop Types")
        fig = px.treemap(df, path=['Store Type Of Location', 'Category', 'Drop Type Of Location'], template='plotly_dark', height=700, color_discrete_sequence=px.colors.qualitative.Bold)
        st.plotly_chart(fig)

        choice = st.radio('Location:', options=('Store', 'Drop'), index = 0, help='Choose the location of the store or drop', horizontal=True)
        st.header(f"{choice} Locations")
        fig = px.sunburst(df, path=[f'{choice} Country', f'{choice} State', f'{choice} City District'], template = 'plotly_dark', height=700, color_discrete_sequence=px.colors.qualitative.Dark24)
        st.plotly_chart(fig)
        
    with tab2:
        def fig1():
            if 'x' not in st.session_state:
                st.session_state.x = st.session_state.x_old = st.session_state.y = st.session_state.y_old = None
                st.session_state.c = st.session_state.c_old = st.session_state.s = st.session_state.s_old = None
                st.session_state.f = st.session_state.f_old = None
                barmode = 'relative'
            def histo():
                st.plotly_chart(px.histogram(data_frame=df.astype('string'), x=st.session_state.x, y=st.session_state.y, color=st.session_state.c, pattern_shape=st.session_state.s, histfunc=st.session_state.f, barmode=barmode, color_discrete_sequence=px.colors.qualitative.Dark24_r))
                
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.session_state.x = st.selectbox(label='x-axis', options=[None] + list(df.columns[1:]), index=0, key = 11)
            with col2:
                st.session_state.y = st.selectbox(label='y-axis', options=[None] + list(df.columns), index=0, key = 12)
            with col3:
                st.session_state.c = st.selectbox(label='color', options=[None] + list(df.select_dtypes('string').columns[1:]), index=0, key = 13)
            with col4:
                st.session_state.s = st.selectbox(label='shape', options=[None] + list(df.select_dtypes('string').columns), index=0, key = 14)
            with col5:
                st.session_state.f = st.selectbox(label='function', options=[None , 'count', 'sum', 'avg', 'min', 'max'], index=0, key = 15)
            barmode = st.radio('Barmode', options=('relative', 'group', 'overlay'), index = 0, horizontal = True)
            
            if st.session_state.x != st.session_state.x_old or st.session_state.y != st.session_state.y_old or st.session_state.c != st.session_state.c_old or st.session_state.s != st.session_state.s_old or st.session_state.f != st.session_state.f_old:
                if st.session_state.y is not None or st.session_state.x is not None:
                    histo()
                st.session_state.x_old = st.session_state.x
                st.session_state.y_old = st.session_state.y
                st.session_state.c_old = st.session_state.c
                st.session_state.s_old = st.session_state.s
        def fig2():
            st.header("Filter by Vehicle Type")
            vehicle_type = st.selectbox("Select Vehicle Type", df['Vehicle'].unique())
            filtered_data = df[df['Vehicle'] == vehicle_type]
            AgGrid(filtered_data)
        fig1()
        fig2()

elif page == "Maps":
    with open('./animations/paper-map-animate.svg', 'r') as file:
        svg_content = file.read()
    st.markdown(f"<div style='width: 300px; height: 300px; align: center'>{svg_content}</div>", unsafe_allow_html=True)
    st.title("Maps")
    tab1, tab2 = st.tabs(['Map Analysis', 'Advanceed Map Analysis'])
    with tab1:
        st.header("Store Locations")
        fig = px.scatter_mapbox(df, lat='Store Latitude', lon='Store Longitude', color='Store City District', zoom=2, height=300)
        fig.update_layout(mapbox_style="open-street-map")
        st.plotly_chart(fig)
        
        st.header("Drop Locations")
        fig = px.scatter_mapbox(df, lat='Drop Latitude', lon='Drop Longitude', color='Drop City District', zoom=2, height=300)
        fig.update_layout(mapbox_style="open-street-map")
        st.plotly_chart(fig)
    with tab2:
        @st.cache_data
        def load_kepler():
            with open('./kepler.gl.html', 'r') as file:
                html_content = file.read()
            return html_content
        components.html(load_kepler(), height=600)
        @st.cache_data
        def load_folium():
            center_lat = (df['Drop Latitude'].mean() + df['Store Latitude'].mean())/2
            center_lon = (df['Drop Longitude'].mean() + df['Store Longitude'].mean())/2
            mymap = folium.Map(location=[center_lat, center_lon], zoom_start=3, tiles='CartoDB dark_matter')
            marker_cluster = MarkerCluster().add_to(mymap)
            def markers(row):
                folium.Marker(
                    location=[row['Store Latitude'], row['Store Longitude']],
                    popup=f"Lat: {row['Store Latitude']}<br>Lon: {row['Store Longitude']}",
                    tooltip=f"{row['Order ID']}",
                    icon=folium.Icon(color='darkred', icon='fa-solid fa-store', icon_color='white', prefix = 'fa')
                ).add_to(marker_cluster)
                folium.Marker(
                    location=[row['Drop Latitude'], row['Drop Longitude']],
                    popup=f"Lat: {row['Drop Latitude']}<br>Lon: {row['Drop Longitude']}",
                    tooltip=f"{row['Order ID']}",
                    icon=folium.Icon(color='darkred', icon='fa-solid fa-truck-ramp-box', icon_color='white', prefix = 'fa')
                ).add_to(marker_cluster)

            df.apply(markers, axis = 1)
            return mymap
        m = load_folium()
        st_folium(m, width=700, height=500)

elif page == "Agent Performance":
    with open('./animations/delivery-animate2.svg', 'r') as file:
        svg_content = file.read()
    st.markdown(f"<div style='width: 300px; height: 300px; align: center'>{svg_content}</div>", unsafe_allow_html=True)
    st.title("Agent Performance")
    
    st.header("Agent Rating Distribution")
    fig = px.histogram(df.astype('string'), x=df['Agent Rating'].astype('string'))
    st.plotly_chart(fig)
    
    st.header("Agent Age Distribution")
    fig = px.histogram(df.astype('string'), x='Agent Age')
    st.plotly_chart(fig)
    
    st.header("Filter by Agent Rating")
    rating = st.slider("Select Rating", min_value=0.0, max_value=5.0, value=(0.0, 5.0))
    filtered_data = df[(df['Agent Rating'] >= rating[0]) & (df['Agent Rating'] <= rating[1])]
    st.write(filtered_data)

st.sidebar.title("Settings")
if st.sidebar.checkbox("Show raw data"):
    st.subheader("Raw Data")
    st.write(df)
