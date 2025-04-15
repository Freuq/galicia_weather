import streamlit as st
import pandas as pd
import plotly.express as px
import folium
import streamlit.components.v1 as components
import tempfile
import os
from utils.filters import *

# Diseño de la página
st.set_page_config(layout="wide")
cargar_css("app/static/styles.css")

st.title("⛅Morriña en Galicia")

localidades = ["Galicia", "Santiago", "A Coruña", "Lugo", "Ourense", "Pontevedra", "Vigo"]
localizacion = st.sidebar.selectbox("Clima en:", localidades)


# Cargar datos
df = cargar_df(localizacion)

# Aplicar filtros desde el archivo utils/filters.py
df_filtrado, año, mes = aplicar_filtros(df)


st.subheader(f"📍 Localización: {localizacion}")
#st.markdown("<br>", unsafe_allow_html=True)

# Crear el mapa
m = folium.Map(location=[42.8782, -8.5448], zoom_start=13, control_scale=False)

# Agregar marcador con emoji y popup en una sola línea
folium.Marker(
    [42.8782, -8.5448],
    icon=folium.DivIcon(html='<div style="font-size:24px;">📍</div>')
).add_to(m)

# Guardar como archivo temporal
with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.html') as f:
    m.save(f.name)
    map_html = f.read()

# Forzar estilo en div padre e iframe
st.components.v1.html(f"""
    <div style="width: 100%; height: 520px; border-radius: 15px; overflow: hidden; border: none;">
        <iframe srcdoc='{map_html}' style="width: 100%; height: 100%; border: none;"></iframe>
    </div>
""", height=520)


df_filtrado["llovio"] = df_filtrado["precipitacion"] > 0
conteo = df_filtrado["llovio"].value_counts().rename({True: "Días con lluvia 🌧️", False: "Días sin lluvia ☀️"}).reset_index()
conteo.columns = ["Tipo de día", "Cantidad"]
if conteo.iloc[0][0] == 'Días sin lluvia ☀️':
    colores = ['#FFEB3B', '#4FC3F7']
else:
    colores = ['#4FC3F7', '#FFEB3B']

# Agrupamos por mes y sumamos las precipitaciones
precipitaciones_mes = df_filtrado.groupby('mes_nombre')['precipitacion'].sum()

# Encontramos el mes con más lluvia
mes_mas_lluvioso = precipitaciones_mes.idxmax()
lluvia_mas = precipitaciones_mes.max()

# Encontramos el mes con menos lluvia
mes_menos_lluvioso = precipitaciones_mes.idxmin()
lluvia_menos = precipitaciones_mes.min()

# Contamos el número total de meses (con datos)
total_meses = len(df_filtrado.groupby('mes_num')['precipitacion'].sum())

################# PRECIPITACIÓN
# Lluvia en Santiago
st.markdown(
    "<h3 style='text-align: center;'>☔ Choiva en Santiago de Compostela</h3>",
    unsafe_allow_html=True
)

fig_pie = px.pie(conteo, title="         Cantidad y porcentaje de días con y sin lluvia en Santiago", names="Tipo de día", values="Cantidad")
fig_pie.update_traces(
    textinfo="percent+label+value", 
    marker=dict(
        colors=colores))
fig_pie.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',  # Fondo de la gráfica transparente
    paper_bgcolor='rgba(0, 0, 0, 0)',  # Fondo del paper transparente
    font=dict(color='white'),
    title_font=dict(color='white'),
    legend=dict(font=dict(color='white')),
    xaxis=dict(title='Fecha', color='white'),
    yaxis=dict(title='Precipitación (L/m²)',
        color='white', 
        gridcolor='rgba(255, 255, 255, 0.4)'),
    autosize=True,
    margin=dict(l=20, r=20, t=40, b=40)
)
fig2 = px.bar(x=[1, 2, 3, 4], y=[4, 5, 6, 7], labels={'x': 'Categorías', 'y': 'Valor'})
# Crear tres columnas
col1, col2 = st.columns(2)

# Colocar cada gráfico en su columna respectiva
with col1:
    st.plotly_chart(fig_pie)

with col2:
    subcol1, subcol2, subcol3 = st.columns(3)
    
    with subcol1:
        st.markdown("<h4 style='text-align: center;'>Recuento en días</h4>", unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Días totales</h5><h2 >{}</h2></div>".format(len(df_filtrado)), unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Días con lluvia</h5><h2 >{}</h2></div>".format((df_filtrado["precipitacion"] > 0).sum()), unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Días sin lluvia</h5><h2 >{}</h2></div>".format((df_filtrado["precipitacion"] == 0).sum()), unsafe_allow_html=True)
    
    with subcol2:
        st.markdown("<h4 style='text-align: center;'>Cantidad (L/m2)</h4>", unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Total</h5><h2 >{:.1f}</h2></div>".format(df_filtrado['precipitacion'].sum()), unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Promedio</h5><h2 >{}</h2></div>".format(round(df_filtrado['precipitacion'].mean(), 2)), unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Maximo</h5><h2 >{}</h2></div>".format((df_filtrado["precipitacion"]).max()), unsafe_allow_html=True)
        
    with subcol3:
        st.markdown("<h4 style='text-align: center;'>En meses</h4>", unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Meses totales</h5><h2 >{}</h2></div>".format(total_meses), unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Mes más lluvioso</h5><h2 >{}</h2></div>".format(mes_mas_lluvioso), unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Mes menos lluvioso</h5><h2 >{}</h2></div>".format(mes_menos_lluvioso), unsafe_allow_html=True)



# Lluvia diaria
fig_rain = px.bar(df_filtrado, x="fecha", y="precipitacion", title="         Precipitación diaria en Santiago de Compostela")
fig_rain.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',  # Fondo de la gráfica transparente
    paper_bgcolor='rgba(0, 0, 0, 0)',  # Fondo del paper transparente
    font=dict(color='white'),
    title_font=dict(color='white'),
    legend=dict(font=dict(color='white')),
    xaxis=dict(title='Fecha', color='white'),
    yaxis=dict(title='Precipitación (L/m²)',
        color='white', 
        gridcolor='rgba(255, 255, 255, 0.4)'),
    autosize=True,
    margin=dict(l=20, r=20, t=40, b=40)
)


st.plotly_chart(fig_rain, use_container_width=True)

############### TEMPERATURA
st.markdown(
    "<h3 style='text-align: center;'>🌡️ Temperatura en Santiago</h3>",
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)
col1.markdown("<div style='text-align: center;'><h5 style='padding-bottom: 0.1px;';'>Promedio (ºC)</h5><h2 >{}</h2></div>".format(round(df_filtrado['temperatura'].mean(), 2)), unsafe_allow_html=True)
col2.markdown("<div style='text-align: center;'><h5 style='padding-bottom: 0.1px;';'>T máxima (ºC)</h5><h2 >{}</h2></div>".format(df_filtrado['temperatura'].max()), unsafe_allow_html=True)
col3.markdown("<div style='text-align: center;'><h5 style='padding-bottom: 0.1px;';'>T mínima (ºC)</h5><h2 >{:.1f}</h2></div>".format(df_filtrado['temperatura'].min()), unsafe_allow_html=True)

# Temperatura diaria

fig_temp = px.line(df_filtrado, x="fecha", y="temperatura", title="         Temperatura media diaria en Santiago")
fig_temp.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',  # Fondo de la gráfica transparente
    paper_bgcolor='rgba(0, 0, 0, 0)',  # Fondo del paper transparente
    font=dict(color='white'),
    title_font=dict(color='white'),
    legend=dict(font=dict(color='white')),
    xaxis=dict(title='Fecha', color='white'),
    yaxis=dict(title='Temperatura (ºC)',
        color='white', 
        gridcolor='rgba(255, 255, 255, 0.4)'),
    autosize=True,
    margin=dict(l=20, r=20, t=40, b=40)
)

st.plotly_chart(fig_temp, use_container_width=True)

################ HUMEDAD RELATIVA
# Visualización: lluvia y temperatura
st.markdown(
    "<h3 style='text-align: center;'>🌫️ Humidade Relativa en Santiago de compostela</h3>",
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)
col1.markdown("<div style='text-align: center;'><h5 style='padding-bottom: 0.1px;';'>Humedad prom (%)</h5><h2 >{}</h2></div>".format(round(df_filtrado['humedad'].mean(), 2)), unsafe_allow_html=True)
col2.markdown("<div style='text-align: center;'><h5 style='padding-bottom: 0.1px;';'>Humedad max (%)</h5><h2 >{}</h2></div>".format(df_filtrado['humedad'].max()), unsafe_allow_html=True)
col3.markdown("<div style='text-align: center;'><h5 style='padding-bottom: 0.1px;';'>Humedad min (%)</h5><h2 >{:.1f}</h2></div>".format(df_filtrado['humedad'].min()), unsafe_allow_html=True)

