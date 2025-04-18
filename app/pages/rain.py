import streamlit as st
import pandas as pd
import plotly.express as px
from utils.filters import *
from utils.df_functions import *

st.set_page_config(layout="wide")
st.markdown("<br>", unsafe_allow_html=True)
st.title("🌧️ Análisis de Lluvia")

def cargar_css(path: str):
    with open(path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Llama a la función
cargar_css("app/static/styles.css")

# Cargar tu dataframe (esto puedes adaptarlo si usas session_state o carga desde archivo)
# Cargar datos
if "df_climatico" not in st.session_state:
    localizacion, localizacion_var = local()
    st.session_state["df_climatico"] = cargar_df(localizacion_var, localidades)

df = st.session_state["df_climatico"]

if df is None:
    st.warning("No se ha encontrado el DataFrame. Asegúrate de cargar los datos primero en la página principal.")
    st.stop()

df_filtrado, año, mes = aplicar_filtros(df)

# Filtros principales
ciudades = df['ciudad'].unique().tolist()
ciudad_seleccionada = st.selectbox("Selecciona una ciudad:", ciudades)
df_filtrado = df[df['ciudad'] == ciudad_seleccionada]

# KPIs / Métricas clave
dias_lluvia = df_filtrado[df_filtrado['precipitacion'] > 0].shape[0]
total_dias = df_filtrado.shape[0]
porcentaje_lluvia = round((dias_lluvia / total_dias) * 100, 2)
mes_mas_lluvioso = df_filtrado.groupby("mes_num")["precipitacion"].sum().idxmax()

col1, col2, col3 = st.columns(3)
col1.metric("🌧️ Días con lluvia", dias_lluvia)
col2.metric("📊 % de días con lluvia", f"{porcentaje_lluvia}%")
col3.metric("📅 Mes más lluvioso", mes_mas_lluvioso)

st.markdown("---")

# Gráfico 1: Línea de precipitación diaria
fig_linea = px.line(df_filtrado, x="fecha", y="precipitacion", title="Evolución diaria de la precipitación")
fig_linea.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    font=dict(color='white'),
    title_font=dict(color='white'),
    xaxis=dict(color='white'),
    yaxis=dict(color='white', gridcolor='rgba(255,255,255,0.4)')
)
st.plotly_chart(fig_linea, use_container_width=True)

# Aquí irían más visualizaciones: histograma, boxplot, clasificación...

st.markdown("---")
st.caption("Datos analizados para la ciudad seleccionada.")