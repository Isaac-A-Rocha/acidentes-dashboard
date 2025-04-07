import folium
from folium.plugins import MarkerCluster
def gerar_mapa(df):
    # Cria um mapa centrado na área de Porto Alegre
    mapa = folium.Map(location=[-30.1, -51.15], zoom_start=11, control_scale=True)

    # Adiciona um cluster para não sobrecarregar o mapa
    cluster = MarkerCluster().add_to(mapa)

    # Apenas latitude e longitude, sem popup nem tooltip
    for lat, lon in df[['latitude', 'longitude']].dropna().itertuples(index=False):
        folium.CircleMarker(
            location=[lat, lon],
            radius=2,  # marcador pequeno
            color='red',
            fill=True,
            fill_opacity=0.6
        ).add_to(cluster)

    return mapa

