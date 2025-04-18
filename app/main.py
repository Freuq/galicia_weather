import streamlit as st
from utils.filters import *
from utils.graphics import *
from utils.df_functions import *

# Diseño de la página
st.set_page_config(layout="wide", page_title="Morriña en Galicia", page_icon="⛅")
cargar_css("app/static/styles.css")
# Configuración de la página

st.title("⛅Morriña en Galicia")

localidades = {
    "galicia": "Galicia",
    "santiago": "Santiago de Compostela",
    "coruna": "Coruña",
    "lugo": "Lugo",
    "ourense": "Ourense",
    "pontevedra": "Pontevedra",
    "vigo": "Vigo"}

localizacion, localizacion_var = local(page_name='main')

st.subheader(f"📍 Localización: {localizacion}")

# Cargar datos
df = cargar_df(localizacion_var, localidades)

# Aplicar filtros desde el archivo utils/filters.py
df_filtrado, año, mes = aplicar_filtros(df)

if "df_climatico" not in st.session_state:
    st.session_state["df_climatico"] = df

# MAPA
map_html = map_local(localizacion_var)

# Forzar estilo en div padre e iframe
st.components.v1.html(f"""
    <div style="width: 100%; height: 520px; border-radius: 15px; overflow: hidden; border: none;">
        <iframe srcdoc='{map_html}' style="width: 100%; height: 100%; border: none;"></iframe>
    </div>
""", height=520)

# GENERACIÓN DE DF_GROUPED (VALORES AGRUPADOS PARA GALICIA) Y DF_CONTEO (NRO DE DÍAS CON LLUVIA Y SIN LLUVIA)
df_grouped, df_conteo = df_grouped_conteo(df_filtrado)
st.markdown("---")
####################################################### PRECIPITACIÓN #######################################################
st.markdown(
    f"<h2 style='text-align: center;'>☔ Choiva en {localizacion}</h2>",
    unsafe_allow_html=True
)

# PIE PLOT: DÍAS CON LLUVIA
fig_pie = lluvia_pie(df_conteo, localizacion)

# VALORES DE LLUVIA MENSUALES
total_meses, mes_mas_lluvioso, mes_menos_lluvioso = lluvia_mensual(df_filtrado)

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
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Total</h5><h2 >{}</h2></div>".format(int(df_grouped['precipitacion'].sum())), unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Promedio</h5><h2 >{}</h2></div>".format(round(df_grouped['precipitacion'].mean(), 2)), unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Maximo</h5><h2 >{}</h2></div>".format((df_grouped["precipitacion"]).max()), unsafe_allow_html=True)
        
    with subcol3:
        st.markdown("<h4 style='text-align: center;'>En meses</h4>", unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Meses totales</h5><h2 >{}</h2></div>".format(total_meses), unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Más lluvioso</h5><h2 >{}</h2></div>".format(mes_mas_lluvioso), unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Menos lluvioso</h5><h2 >{}</h2></div>".format(mes_menos_lluvioso), unsafe_allow_html=True)

# lluvia mensual
fig_rain_monthly = plot_lluvia_mes(df_filtrado, localizacion)
st.plotly_chart(fig_rain_monthly, use_container_width=True)
st.markdown("---")
################################################### TEMPERATURA #######################################################
st.markdown(
    f"<h2 style='text-align: center;'>🌡️ Temperatura en {localizacion}</h2>",
    unsafe_allow_html=True
)

# BARPLOT TEMPERATURA: VARIABLE CATEGÓRICA
categorias = {'Frío❄️ (<10°C)':10, 
              'Templado🌤️ (10–20°C)':20,
              'Cálido♨️ (>20°C)':30}

df_temp_cat = df_categorico(df_filtrado, 'temperatura', categorias)
fig_temp_cat = fig_bar_temp_cat(df_temp_cat)
#st.plotly_chart(fig_temp_cat, use_container_width=True)

col1, col2 = st.columns([2, 1])  # 2 partes y 1 parte → 66% y 33%

with col1:
    st.plotly_chart(fig_temp_cat)

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>🔥 Temperatura máxima</h5><h2 >{} ºC</h2></div>".format(round(df_grouped['temperatura'].max(), 2)), unsafe_allow_html=True)
    st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>⚖️ Temperatura promedio</h5><h2 >{} ºC</h2></div>".format(round(df_grouped['temperatura'].mean(), 2)), unsafe_allow_html=True)
    st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>🧊 Temperatura mínima</h5><h2 >{} ºC</h2></div>".format(df_grouped['temperatura'].min()), unsafe_allow_html=True)

# LINEA DE TEMPERATURA DIARIA: Muestra la evolución temporal y diferencias entre ciudades
#fig_temp_line = plot_temp_line(df_filtrado, localizacion)
#st.plotly_chart(fig_temp_line, use_container_width=True)

# LINEA DE TEMPERATURA MENSUAL: Muestra la evolución temporal y diferencias entre ciudades POR MES
fig_temp_monthly = plot_temp_mes(df_filtrado, localizacion)
st.plotly_chart(fig_temp_monthly, use_container_width=True)

# BOXPLOT POR MES: Permite ver la dispersión, medianas y outliers por mes
fig_temp_boxplot = plot_temp_boxplot(df_filtrado, localizacion)
st.plotly_chart(fig_temp_boxplot, use_container_width=True)

# MEDIA MENSUAL POR CIUDAD (LINEA O BARRAS):  Buena para ver estacionalidad y comparaciones regionales
#fig_temp_monthly_avg = plot_temp_monthly_avg(df_filtrado, localizacion)
#st.plotly_chart(fig_temp_monthly_avg, use_container_width=True)
st.markdown("---")
########################################### HUMEDAD RELATIVA #######################################################
st.markdown(
    f"<h2 style='text-align: center;'>🌫️ Humidade Relativa en {localizacion}</h2>",
    unsafe_allow_html=True
)

# BARPLOT CATEGORICO
categorias = {'Seco 🌵 (<50%)':50, 
              'Moderado 🌤️ (50–75%)':75,
              'Húmedo 💧 (>75%)':100}
colores = {
    'Seco 🌵 (<50%)': 'rgb(204, 204, 204)',  # Gris claro para baja humedad
    'Moderado 🌤️ (50–75%)': 'rgb(102, 153, 255)',  # Azul claro para humedad moderada
    'Húmedo 💧 (>75%)': 'rgb(7, 121, 197)' # Azul fuerte para alta humedad
}

df_hum_cat = df_categorico(df_filtrado, 'humedad', categorias)
fig_bar_hum = fig_bar_humedad(df_hum_cat, colores)
#st.plotly_chart(fig_bar_hum, use_container_width=True)

col1, col2 = st.columns([2, 1])  # 2 partes y 1 parte → 66% y 33%

with col1:
    st.plotly_chart(fig_bar_hum, use_container_width=True)

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>🔼 Humedad máxima</h5><h2 >{} %</h2></div>".format(round(df_grouped['humedad'].max(), 2)), unsafe_allow_html=True)
    st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>➖ Humedad promedio</h5><h2 >{} %</h2></div>".format(round(df_grouped['humedad'].mean(), 2)), unsafe_allow_html=True)
    st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>🔽 Humedad mínima</h5><h2 >{:.1f} %</h2></div>".format(df_grouped['humedad'].min()), unsafe_allow_html=True)


# LINEA DE HUMEDAD DIARIA: Muestra la evolución temporal y diferencias entre ciudades
#fig_humidity_line = plot_humidity_line(df_filtrado, localizacion)
#st.plotly_chart(fig_humidity_line, use_container_width=True)

# LINEA DE HUMEDAD MENSUAL
fig_hume_mes = plot_hum_mes(df_filtrado, localizacion)
st.plotly_chart(fig_hume_mes, use_container_width=True)

# DISTRIBUCIÓN DE HUMEDAD (HISTOGRAMA O UN KDE): Te dice en qué rango de humedad se mueven la mayoría de los días
fig_humidity_kde_clean = plot_humidity_kde_line(df_filtrado, localizacion)
st.plotly_chart(fig_humidity_kde_clean, use_container_width=True)

# MAPA DE CALOR (HEATMAP): Muy visual para ver tendencias, anomalías o días con humedad alta/baja
if localizacion_var == "galicia":
    fig_humidity_heatmap = plot_humidity_heatmap(df_filtrado, localizacion)
    st.plotly_chart(fig_humidity_heatmap, use_container_width=True)

####################################### COMPARATIVAS #######################################################
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    f"<h2 style='text-align: center;'>Temperatura vs Humidade en {localizacion}</h2>",
    unsafe_allow_html=True
)

# SCATTER PLOT ENTRE TEMP Y HUMEDAD: Para ver correlaciones o agrupaciones
fig_temp_vs_humidity = plot_temp_vs_humidity(df_filtrado, localizacion)
st.plotly_chart(fig_temp_vs_humidity, use_container_width=True)

# LINEA CON DOBLE EJE Y: Útil para ver cómo cambian juntas en el tiempo
fig_temp_humidity = plot_temp_humidity_dual_axis(df_grouped, localizacion)
st.plotly_chart(fig_temp_humidity, use_container_width=True)