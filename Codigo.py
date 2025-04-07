import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster

# Cargar shapefile de Nueva Esparta
nueva_esparta = gpd.read_file("data/gadm41_VEN_2.shp")
nueva_esparta = nueva_esparta[nueva_esparta["NAME_1"] == "Nueva Esparta"]

# Cargar CSV con "Asic"
df = pd.read_csv("data/riesgo_oropouche.csv")

# Convertir a GeoDataFrame
gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df.Longitud, df.Latitud),
    crs="EPSG:4326"
)

# Crear mapa
m = folium.Map(location=[11.0, -64.0], zoom_start=10)

# Capa de límites geográficos
folium.GeoJson(
    nueva_esparta,
    style_function=lambda x: {"fillColor": "#cccccc", "color": "#000000", "weight": 1}
).add_to(m)

# Capa de puntos con filtros por Asic
marker_cluster = MarkerCluster().add_to(m)
color_map = {"Alto": "#FF0000", "Medio": "#FFA500", "Bajo": "#00FF00"}

for _, row in gdf.iterrows():
    popup_content = f"""
    <div style='font-size: 16px;'>
    <b>Asic:</b> {row["Asic"]}<br>
    <b>Municipio:</b> {row["Municipio"]}<br>
    <b>Zona:</b> {row["Zona"]}<br>
    <b>Riesgo:</b> {row["Riesgo"]}<br>
    <b>Notas:</b> {row["Notas"]}
    """
    folium.CircleMarker(
        location=[row["Latitud"], row["Longitud"]],
        radius=20,
        color=color_map[row["Riesgo"]],
        fill=True,
        fill_color=color_map[row["Riesgo"]],
        fill_opacity=0.7,
        popup=folium.Popup(popup_content, max_width=500)
    ).add_to(marker_cluster)

# Leyenda
legend_html = """
<div style="
    position: fixed; 
    bottom: 50px; 
    left: 50px; 
    width: 190px; 
    height: 120px; 
    border: 2px solid grey; 
    background: white; 
    padding: 10px;
    z-index: 9999;
">
    <b>Leyenda:</b><br>
    <i class="fa fa-circle" style="color:#FF0000"></i> Riesgo Alto (65-85%)<br>
    <i class="fa fa-circle" style="color:#FFA500"></i> Riesgo Medio (35-60%)<br>
    <i class="fa fa-circle" style="color:#00FF00"></i> Riesgo Bajo (10-30%)
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# Guardar mapa
m.save("mapa_riesgo_oropouche.html")

print("Mapa actualizado")