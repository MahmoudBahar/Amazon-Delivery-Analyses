import streamlit as st
import plotly.express as px
import streamlit.components.v1 as components
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import requests

# with open('./animations/paper-map-animate.svg', 'r') as file:
#     svg_content = file.read()
st.markdown(f"<div style='width: 300px; height: 300px; align: center'>{requests.get("https://raw.githubusercontent.com/MahmoudBahar/Amazon-Delivery-Analyses/main/StreamLit/animations/paper-map-animate.svg").content.decode('utf-8')}</div>", unsafe_allow_html=True)
st.title("Maps")
tab1, tab2 = st.tabs(['Map Analysis', 'Advanceed Map Analysis'])
with tab1:
    st.header("Store Locations")
    fig = px.scatter_mapbox(st.session_state.df, lat='Store Latitude', lon='Store Longitude', color='Store City District', zoom=2, height=300)
    fig.update_layout(mapbox_style="carto-darkmatter")
    st.plotly_chart(fig)
    
    st.header("Drop Locations")
    fig = px.scatter_mapbox(st.session_state.df, lat='Drop Latitude', lon='Drop Longitude', color='Drop City District', zoom=2, height=300)
    fig.update_layout(mapbox_style="carto-darkmatter")
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
        center_lat = (st.session_state.df['Drop Latitude'].mean() + st.session_state.df['Store Latitude'].mean())/2
        center_lon = (st.session_state.df['Drop Longitude'].mean() + st.session_state.df['Store Longitude'].mean())/2
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

        st.session_state.df.reset_index().apply(markers, axis = 1)
        return mymap
    m = load_folium()
    st_folium(m, width=700, height=500)
