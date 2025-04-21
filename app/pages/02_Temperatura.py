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
df_gal["mes"] = df_gal["fecha"].dt.to_period("M")
# Agrupamos por ciudad
df_kpi = df_gal.groupby("ciudad")

# Ciudad menos humeda
ciudad_menos_temp, valor_menos_temp = obtiene_minimo(df_kpi, 'temperatura')

# Ciudad más humeda
ciudad_mas_temp, valor_mas_temp = obtiene_maximo(df_kpi, 'temperatura')

# Ciudad con pico más frío (mínima temperatura)
ciudad_mas_fria_pico = df_kpi["temperatura"].min().idxmin()
pico_mas_frio = df_kpi["temperatura"].min().min()

# Ciudad con pico más cálido (máxima temperatura)
ciudad_mas_calida_pico = df_kpi["temperatura"].max().idxmax()
pico_mas_calido = df_kpi["temperatura"].max().max()

# Mes menor temp, mes mayor temp
mes_menor_temp, mes_mayor_temp = max_min_func(df_gal, 'mes', 'temperatura', 'median')
mes_menor_temp_nombre, mes_menor_temp_valor = mes_menor_temp
mes_mayor_temp_nombre, mes_mayor_temp_valor = mes_mayor_temp

# Dia menor temp, dia mayor temp
min_temp, max_temp = max_min_func(df_gal, "fecha", 'temperatura', 'median')
fecha_min, valor_min = min_temp
fecha_max, valor_max = max_temp


# Mostrar métricas
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("❄️ Ciudad más fría", ciudad_menos_temp, f"{valor_menos_temp:.2f} °C", delta_color="off")
    st.metric("🌞 Ciudad más calurosa", ciudad_mas_temp, f"{valor_mas_temp:.2f} °C", delta_color="off")
with col2:
    st.metric("❄️ Ciudad con pico más frío", ciudad_mas_fria_pico, f"{pico_mas_frio:.2f} °C", delta_color="off")
    st.metric("🌞 Ciudad con pico más caluroso", ciudad_mas_calida_pico, f"{pico_mas_calido:.2f} °C", delta_color="off")
with col3:
    st.metric("📆🧊 Día más frío", pd.to_datetime(fecha_min).strftime("%d %b %Y"), f"{valor_min:.2f} °C", delta_color="off")
    st.metric("📆🔥 Día más caluroso", pd.to_datetime(fecha_max).strftime("%d %b %Y"), f"{valor_max:.2f} °C", delta_color="off")
with col4:
    st.metric("📅🌬️ Mes más frío", str(mes_menor_temp_nombre.strftime("%B %Y")), f"{mes_menor_temp_valor:.2f} °C", delta_color="off")
    st.metric("📅🌞 Mes más cálido", str(mes_mayor_temp_nombre.strftime("%B %Y")), f"{mes_mayor_temp_valor:.2f} °C", delta_color="off")



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