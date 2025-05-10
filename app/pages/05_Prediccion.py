import streamlit as st
import pandas as pd
import plotly.express as px
from utils.filters import *
from utils.df_functions import *
from utils.graphics import *

st.set_page_config(layout="wide", page_title="Morriña en Galicia - Predicción", page_icon="🌧️")
cargar_css("app/static/styles.css")

# Cargar tu dataframe (esto puedes adaptarlo si usas session_state o carga desde archivo)
# Cargar datos
if "df_climatico" not in st.session_state:
    localizacion, localizacion_var = local(page_name='rain')
    st.session_state["df_climatico"] = cargar_df(localizacion_var, localidades)
else:
    localizacion, localizacion_var = local(page_name='rain')
# Filtros principales
df = st.session_state["df_climatico"]

if df is None:
    st.warning("No se ha encontrado el DataFrame. Asegúrate de cargar los datos primero en la página principal.")
    st.stop()

st.markdown("<br>", unsafe_allow_html=True)
st.title(f"📈 Predicción en Galicia")

df_filtrado, año, mes = aplicar_filtros(df)
df_grouped, df_conteo = df_grouped_conteo(df_filtrado)

st.markdown(
    f"<h3 style='text-align: center;'><a target='_self' style='color: #ffffff;'>Selecciona una Localidad, actualmente estamos en {localizacion}</a></h3>",
    unsafe_allow_html=True
)

