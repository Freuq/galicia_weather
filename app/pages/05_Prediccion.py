import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
from collections import Counter
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


localidades = {
    "galicia": "Galicia",
    "santiago": "Santiago de Compostela",
    "coruna": "Coruña",
    "lugo": "Lugo",
    "ourense": "Ourense",
    "pontevedra": "Pontevedra",
    "vigo": "Vigo"}

localidad = st.selectbox("Selecciona una localidad", localidades)
#fecha = st.date_input("Selecciona la fecha", default=mañana)

def cargar_datos(localidad):
    # Deberías tener un df con columnas: ['hora', 'temperatura', 'humedad', 'tipo_cielo', 'precipitacion']
    df = pd.read_csv(f"data/processed/forecast/{localidad}_forecast.csv")  # o cargar desde dicts en memoria
    df['time'] = pd.to_datetime(df['time'])
    df['hora'] = df['time'].dt.hour
    df["hour"] = df['time'].dt.strftime('%H:%M')
    return df

if df.empty:
    st.warning("No hay datos disponibles para mañana.")
    st.stop()

df = cargar_datos(localidad)

# --- Métricas rápidas
col1, col2, col3 = st.columns(3)
col1.metric("Temp. media 🌡️", f"{df['temperatura'].mean():.1f} °C")
col2.metric("Humedad media 💧", f"{df['humedad'].mean():.0f} %")
col3.metric("Lluvia total 🌧️", f"{df['precipitacion'].sum():.1f} mm")

# --- Estado general del cielo
modo = Counter(df['tipo_cielo']).most_common(1)[0][0]
st.subheader("☁️ Estado general del cielo")
st.write(f"Durante el día predominará un cielo **{modo.lower()}**.")

# --- Gráficas de evolución
st.subheader("📈 Evolución horaria")

tab1, tab2, tab3 = st.tabs(["Temperatura", "Humedad", "Precipitación"])

with tab1:
    st.altair_chart(
        alt.Chart(df).mark_line().encode(
            x='hora:T',
            y=alt.Y('temperatura:Q', title='Temperatura (°C)'),
            tooltip=['hora', 'temperatura']
        ).properties(height=300),
        use_container_width=True
    )

with tab2:
    st.altair_chart(
        alt.Chart(df).mark_line(color='blue').encode(
            x='hora:T',
            y=alt.Y('humedad:Q', title='Humedad (%)'),
            tooltip=['hora', 'humedad']
        ).properties(height=300),
        use_container_width=True
    )

with tab3:
    st.altair_chart(
        alt.Chart(df).mark_bar(color='teal').encode(
            x='hora:T',
            y=alt.Y('precipitacion:Q', title='Precipitación (mm)'),
            tooltip=['hora', 'precipitacion']
        ).properties(height=300),
        use_container_width=True
    )