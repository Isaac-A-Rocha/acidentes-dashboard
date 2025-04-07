import folium
from folium.plugins import MarkerCluster

def gerar_mapa(df):
    mapa = folium.Map(location=[-30.1, -51.15], zoom_start=11)
    cluster = MarkerCluster().add_to(mapa)

    for lat, lon in df[['latitude', 'longitude']].itertuples(index=False):
        folium.Marker([lat, lon]).add_to(cluster)

    return mapa
