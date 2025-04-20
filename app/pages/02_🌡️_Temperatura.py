import streamlit as st
import pandas as pd
import plotly.express as px
from utils.filters import *
from utils.df_functions import *
from utils.graphics import *

st.set_page_config(layout="wide", page_title="Morriña en Galicia - Temperatura", page_icon="🌡️")
cargar_css("app/static/styles.css")

# Cargar tu dataframe (esto puedes adaptarlo si usas session_state o carga desde archivo)
# Cargar datos
if "df_climatico" not in st.session_state:
    localizacion, localizacion_var = local(page_name='temperature')
    st.session_state["df_climatico"] = cargar_df(localizacion_var, localidades)
else:
    localizacion, localizacion_var = local(page_name='temperature')
# Filtros principales
df = st.session_state["df_climatico"]

if df is None:
    st.warning("No se ha encontrado el DataFrame. Asegúrate de cargar los datos primero en la página principal.")
    st.stop()

st.markdown("<br>", unsafe_allow_html=True)
st.title(f"🌡️ Temperatura en Galicia")

df_filtrado, año, mes = aplicar_filtros(df)
df_grouped, df_conteo = df_grouped_conteo(df_filtrado)

################# MÉTRICAS PARA TODA GALICIA
# CIUDAD MÁS FRÍA
# CIUDAD MÁS CÁLIDA
# MES MÁS FRÍO
# MES MÁS CÁLIDO
# DÍA MÁS FRÍO
# DÍA MÁS CÁLIDO
# Agrupamos por ciudad
# Asegurarse de que la columna 'fecha' es datetime
df_gal = df_galicia(localidades)
df_gal["fecha"] = pd.to_datetime(df_gal["fecha"])
# Agrupamos por ciudad
df_kpi = df_gal.groupby("ciudad")

# Ciudad más fría (mínima temperatura)
ciudad_mas_fria = df_kpi["temperatura"].median().idxmin()
temperatura_ciudad_mas_fria = df_kpi["temperatura"].median().min()

# Ciudad más cálida (máxima temperatura)
ciudad_mas_calida = df_kpi["temperatura"].median().idxmax()
temperatura_ciudad_mas_calida = df_kpi["temperatura"].median().max()

# Ciudad con pico más frío (mínima temperatura)
ciudad_mas_fria_pico = df_kpi["temperatura"].min().idxmin()
pico_mas_frio = df_kpi["temperatura"].min().min()

# Ciudad con pico más cálido (máxima temperatura)
ciudad_mas_calida_pico = df_kpi["temperatura"].max().idxmax()
pico_mas_calido = df_kpi["temperatura"].max().max()

# Asegurarse de que la columna 'fecha' es datetime
df_gal["fecha"] = pd.to_datetime(df["fecha"])
# Crear una columna 'mes' en formato año-mes
df_gal["mes"] = df_gal["fecha"].dt.to_period("M")
# Agrupar por mes y sumar la precipitación
precipitacion_por_mes = df_gal.groupby("mes")["precipitacion"].sum()
# Obtener el mes con más precipitación
mes_mas_lluvioso = precipitacion_por_mes.idxmax()
lluvia_total_mes = precipitacion_por_mes.max()


# Mes más frío (mínima temperatura media mensual)
df_gal["mes"] = df_gal["fecha"].dt.to_period("M")
temperatura_media_por_mes = df_gal.groupby("mes")["temperatura"].median()
mes_mas_frio = temperatura_media_por_mes.idxmin()
temperatura_mes_mas_frio = temperatura_media_por_mes.min()

# Mes más cálido (máxima temperatura media mensual)
mes_mas_calido = temperatura_media_por_mes.idxmax()
temperatura_mes_mas_calido = temperatura_media_por_mes.max()

df_dias = df_gal.drop('ciudad', axis = 1).groupby("fecha")["temperatura"].median()

# Día más frío (mínima temperatura)
fecha_mas_frio = df_dias.idxmin()
temperatura_maxima_dia_frio = df_dias.min()

# Día más cálido (máxima temperatura)
fecha_mas_calido = df_dias.idxmax()
temperatura_maxima_dia_calido = df_dias.max()

# Mostrar métricas
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("❄️ Ciudad más fría", ciudad_mas_fria, f"{temperatura_ciudad_mas_fria:.2f} °C", delta_color="off")
    st.metric("🌞 Ciudad más calurosa", ciudad_mas_calida, f"{temperatura_ciudad_mas_calida:.2f} °C", delta_color="off")
with col2:
    st.metric("❄️ Ciudad con pico más frío", ciudad_mas_fria_pico, f"{pico_mas_frio:.2f} °C", delta_color="off")
    st.metric("🌞 Ciudad con pico más caluroso", ciudad_mas_calida_pico, f"{pico_mas_calido:.2f} °C", delta_color="off")
with col3:
    st.metric("📆🧊 Día más frío", pd.to_datetime(fecha_mas_frio).strftime("%d %b %Y"), f"{temperatura_maxima_dia_frio:.2f} °C", delta_color="off")
    st.metric("📆🔥 Día más caluroso", pd.to_datetime(fecha_mas_calido).strftime("%d %b %Y"), f"{temperatura_maxima_dia_calido:.2f} °C", delta_color="off")
with col4:
    st.metric("📅🌬️ Mes más frío", str(mes_mas_frio.strftime("%B %Y")), f"{temperatura_mes_mas_frio:.2f} °C", delta_color="off")
    st.metric("📅🌞 Mes más cálido", str(mes_mas_calido.strftime("%B %Y")), f"{temperatura_mes_mas_calido:.2f} °C", delta_color="off")



st.markdown("---")
st.subheader(f"📍 Localización: {localizacion}")
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


# LINEA DE TEMPERATURA MENSUAL: Muestra la evolución temporal y diferencias entre ciudades POR MES
fig_temp_monthly = plot_temp_mes(df_filtrado, localizacion)
st.plotly_chart(fig_temp_monthly, use_container_width=True)

# BOXPLOT POR MES: Permite ver la dispersión, medianas y outliers por mes
fig_temp_boxplot = plot_temp_boxplot(df_filtrado, localizacion)
st.plotly_chart(fig_temp_boxplot, use_container_width=True)

# LINEA DE TEMPERATURA DIARIA: Muestra la evolución temporal y diferencias entre ciudades
fig_temp_line = plot_temp_line(df_filtrado, localizacion)
st.plotly_chart(fig_temp_line, use_container_width=True)