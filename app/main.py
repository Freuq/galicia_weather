import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import folium
import tempfile
import os
from utils.filters import *
from utils.graphics import *

# Diseño de la página
st.set_page_config(layout="wide")
cargar_css("app/static/styles.css")

st.title("⛅Morriña en Galicia")

localidades = ["Galicia", "Santiago", "Coruña", "Lugo", "Ourense", "Pontevedra", "Vigo"]
localizacion = st.sidebar.selectbox("Clima en:", localidades)
st.subheader(f"📍 Localización: {localizacion}")
localizacion_var = localizacion.lower().replace('ñ', 'n')

# Cargar datos
df = cargar_df(localizacion_var)

# Aplicar filtros desde el archivo utils/filters.py
df_filtrado, año, mes = aplicar_filtros(df)

# Crear el mapa
lon, lat = coors(localizacion_var)
zoom = 7.5 if localizacion_var.lower() == 'galicia' else 12

m = folium.Map(location=[lat, lon], zoom_start=zoom, control_scale=False)
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

df_grouped = df_filtrado.groupby('fecha').agg({
    'temperatura': 'mean',
    'precipitacion': 'sum',
    'humedad': 'mean'
}).reset_index()

df_grouped['llovio'] = df_grouped['precipitacion'] > 0
conteo_con = df_grouped["llovio"].sum()
conteo_sin = len(df_grouped) - conteo_con
conteo = [conteo_con, conteo_sin]
conteo = [conteo_con, conteo_sin]
etiquetas = ['Días con lluvia 🌧️', 'Días sin lluvia ☀️']

df_conteo = pd.DataFrame({
    'Tipo de día': etiquetas,
    'Cantidad': conteo
})
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
df_filtrado['mes_anyo'] = df_filtrado['fecha'].dt.to_period('M')
total_meses = df_filtrado['mes_anyo'].nunique()

####################################################### PRECIPITACIÓN #######################################################
# Lluvia en Santiago
st.markdown(
    f"<h3 style='text-align: center;'>☔ Choiva en {localizacion}</h3>",
    unsafe_allow_html=True
)

fig_pie = px.pie(df_conteo, title="         Porcentaje de días con y sin lluvia en Santiago", names="Tipo de día", values="Cantidad")
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

# Crear tres columnas
col1, col2 = st.columns(2)

# Colocar cada gráfico en su columna respectiva
with col1:
    st.plotly_chart(fig_pie)

with col2:
    subcol1, subcol2, subcol3 = st.columns(3)
    
    with subcol1:
        st.markdown("<h4 style='text-align: center;'>En días</h4>", unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Días totales</h5><h2 >{}</h2></div>".format(len(df_grouped)), unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Con lluvia</h5><h2 >{}</h2></div>".format((df_grouped["precipitacion"] > 0).sum()), unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Sin lluvia</h5><h2 >{}</h2></div>".format((df_grouped["precipitacion"] == 0).sum()), unsafe_allow_html=True)
    
    with subcol2:
        st.markdown("<h4 style='text-align: center;'>Cantidad (L/m2)</h4>", unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Total</h5><h2 >{:.1f}</h2></div>".format(int(df_grouped['precipitacion'].sum())), unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Promedio</h5><h2 >{}</h2></div>".format(round(df_grouped['precipitacion'].mean(), 2)), unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Maximo</h5><h2 >{}</h2></div>".format((df_grouped["precipitacion"]).max()), unsafe_allow_html=True)
        
    with subcol3:
        st.markdown("<h4 style='text-align: center;'>En meses</h4>", unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Meses totales</h5><h2 >{}</h2></div>".format(total_meses), unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Más lluvioso</h5><h2 >{}</h2></div>".format(mes_mas_lluvioso), unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Menos lluvioso</h5><h2 >{}</h2></div>".format(mes_menos_lluvioso), unsafe_allow_html=True)



# Lluvia diaria
def plot_lluvia_line(df, localizacion):

    if 'ciudad' in df.columns:
        fig = px.bar(df, x="fecha", y="precipitacion", color="ciudad",
                      title=f"         Temperatura diaria en {localizacion}")
    else:
        fig = px.bar(df, x="fecha", y="precipitacion",
                      title=f"         Temperatura diaria en {localizacion}")

    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='white'),
        title_font=dict(color='white'),
        legend=dict(font=dict(color='white')),
        xaxis=dict(title='Fecha', color='white'),
        yaxis=dict(title='Temperatura (°C)', color='white', gridcolor='rgba(255, 255, 255, 0.4)'),
        autosize=True,
        margin=dict(l=20, r=20, t=40, b=40)
    )
    
    return fig

fig_rain = plot_lluvia_line(df_filtrado, localizacion)

st.plotly_chart(fig_rain, use_container_width=True)

################################################### TEMPERATURA #######################################################
st.markdown(
    f"<h3 style='text-align: center;'>🌡️ Temperatura en {localizacion}</h3>",
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)
col1.markdown("<div style='text-align: center;'><h5 style='padding-bottom: 0.1px;';'>T mínima (ºC)</h5><h2 >{:.1f}</h2></div>".format(df_grouped['temperatura'].min()), unsafe_allow_html=True)
col2.markdown("<div style='text-align: center;'><h5 style='padding-bottom: 0.1px;';'>Promedio (ºC)</h5><h2 >{}</h2></div>".format(round(df_grouped['temperatura'].mean(), 2)), unsafe_allow_html=True)
col3.markdown("<div style='text-align: center;'><h5 style='padding-bottom: 0.1px;';'>T máxima (ºC)</h5><h2 >{}</h2></div>".format(round(df_grouped['temperatura'].max(), 2)), unsafe_allow_html=True)


# LINEA DE TEMPERATURA DIARIA: Muestra la evolución temporal y diferencias entre ciudades
fig_temp_line = plot_temp_line(df_filtrado, localizacion)
st.plotly_chart(fig_temp_line, use_container_width=True)

# BOXPLOT POR MES: Permite ver la dispersión, medianas y outliers por mes
fig_temp_boxplot = plot_temp_boxplot(df_filtrado, localizacion)
st.plotly_chart(fig_temp_boxplot, use_container_width=True)

# MEDIA MENSUAL POR CIUDAD (LINEA O BARRAS):  Buena para ver estacionalidad y comparaciones regionales
fig_temp_monthly_avg = plot_temp_monthly_avg(df_filtrado, localizacion)
st.plotly_chart(fig_temp_monthly_avg, use_container_width=True)

########################################### HUMEDAD RELATIVA #######################################################
st.markdown(
    f"<h3 style='text-align: center;'>🌫️ Humidade Relativa en {localizacion}</h3>",
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)
col1.markdown("<div style='text-align: center;'><h5 style='padding-bottom: 0.1px;';'>Humedad min (%)</h5><h2 >{:.1f}</h2></div>".format(df_grouped['humedad'].min()), unsafe_allow_html=True)
col2.markdown("<div style='text-align: center;'><h5 style='padding-bottom: 0.1px;';'>Humedad prom (%)</h5><h2 >{}</h2></div>".format(round(df_grouped['humedad'].mean(), 2)), unsafe_allow_html=True)
col3.markdown("<div style='text-align: center;'><h5 style='padding-bottom: 0.1px;';'>Humedad max (%)</h5><h2 >{}</h2></div>".format(round(df_grouped['humedad'].max(), 2)), unsafe_allow_html=True)

# LINEA DE TEMPERATURA DIARIA: Muestra la evolución temporal y diferencias entre ciudades
fig_humidity_line = plot_humidity_line(df_filtrado, localizacion)
st.plotly_chart(fig_humidity_line, use_container_width=True)

# DISTRIBUCIÓN DE HUMEDAD (HISTOGRAMA O UN KDE): Te dice en qué rango de humedad se mueven la mayoría de los días
fig_humidity_kde_clean = plot_humidity_kde_line(df_filtrado, localizacion)
st.plotly_chart(fig_humidity_kde_clean, use_container_width=True)

# MAPA DE CALOR (HEATMAP): Muy visual para ver tendencias, anomalías o días con humedad alta/baja
fig_humidity_heatmap = plot_humidity_heatmap(df_filtrado, localizacion)
st.plotly_chart(fig_humidity_heatmap, use_container_width=True)

####################################### COMPARATIVAS #######################################################
st.markdown(
    f"<h3 style='text-align: center;'>Temperatura vs Humidade en {localizacion}</h3>",
    unsafe_allow_html=True
)

# SCATTER PLOT ENTRE TEMP Y HUMEDAD: Para ver correlaciones o agrupaciones
fig_temp_vs_humidity = plot_temp_vs_humidity(df_filtrado, localizacion)
st.plotly_chart(fig_temp_vs_humidity, use_container_width=True)

# LINEA CON DOBLE EJE Y: Útil para ver cómo cambian juntas en el tiempo
fig_temp_humidity = plot_temp_humidity_dual_axis(df_grouped, localizacion)
st.plotly_chart(fig_temp_humidity, use_container_width=True)