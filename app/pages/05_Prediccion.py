import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta
from collections import Counter
from utils.filters import *
from utils.df_functions import *
from utils.graphics import *
from utils.forecast import *

st.set_page_config(layout="wide", page_title="Morriña en Galicia - Predicción", page_icon="🌤️")
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
st.title(f"🌤️ Predicción en Galicia")

#df_filtrado, año, mes = aplicar_filtros(df)
#df_grouped, df_conteo = df_grouped_conteo(df_filtrado)

localidades = {
    "santiago": "Santiago de Compostela",
    "coruna": "Coruña",
    "lugo": "Lugo",
    "ourense": "Ourense",
    "pontevedra": "Pontevedra",
    "vigo": "Vigo"}

df_fore = forecast_main(localidades)

localidad = st.selectbox("Selecciona una localidad", localidades.values())

df = df_fore[df_fore['city'] == localidad]

hoy = date.today()
tomorrow = (hoy + timedelta(days=1)).isoformat()
#fecha = st.date_input("Selecciona la fecha", default=mañana) 
st.markdown(
    f"<h3 style='text-align: center;'>Clima para mañana ({tomorrow}) en {localidad}</h3>",
    unsafe_allow_html=True
)

if df.empty:
    st.warning("No hay datos disponibles para mañana.")
    st.stop()
##################################################################################
# --- Métricas rápidas

col4, col5, col6 = st.columns(3)
with col4:
    st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>🌡️ Temperatura media</h5><h2 >{}</h2></div>".format(f"{df['temperature'].mean():.1f} °C"), unsafe_allow_html=True)
with col5:
    st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>💧 Humedad media</h5><h2 >{}</h2></div>".format(f"{df['humidity'].mean():.0f} %"), unsafe_allow_html=True)
with col6:
    st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>🌧️ Lluvia total</h5><h2 >{}</h2></div>".format(f"{df['precipitation'].sum():.1f} L/m2"), unsafe_allow_html=True)

##################################################################################
# --- Estado general del cielo
modo = Counter(df['sky_state']).most_common(1)[0][0]
sky = {
    "SUNNY": "Despejado ☀️",
    "HIGH_CLOUDS": "Nubes altas 🌤️",
    "PARTLY_CLOUDY": "Parcialmente nublado 🌥️",
    "OVERCAST": "Cubierto ☁️",
    "CLOUDY": "Nublado 🌥️",
    "FOG": "Niebla 🌫️",
    "SHOWERS": "Chubascos 🌦️",
    "OVERCAST_AND_SHOWERS": "Cubierto con chubascos 🌧️",
    "INTERMITENT_SNOW": "Nieve intermitente ❄️",
    "DRIZZLE": "Llovizna 🌦️",
    "RAIN": "Lluvia 🌧️",
    "SNOW": "Nieve ❄️",
    "STORMS": "Tormentas ⛈️",
    "MIST": "Neblina 🌫️",
    "FOG_BANK": "Banco de niebla 🌫️",
    "MID_CLOUDS": "Nubes medias 🌥️",
    "WEAK_RAIN": "Lluvia débil 🌦️",
    "WEAK_SHOWERS": "Chubascos débiles 🌦️",
    "STORM_THEN_CLOUDY": "Tormenta y luego nublado ⛈️☁️",
    "MELTED_SNOW": "Nieve derretida 💧❄️",
    "RAIN_HayL": "Lluvia con granizo 🌧️🌨️"
}

st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>☁️ Estado general del cielo</h5><h2 >{}</h2></div>".format(f"{sky[modo]}"), unsafe_allow_html=True)

st.markdown("---")
#######################################################################
# --- Gráficas de evolución
st.markdown(
    f"<h2 style='text-align: center;'>📈 Predicción del clima a lo largo del día</h2>",
    unsafe_allow_html=True
)
fig1 = px.line(df, x="hour", y="temperature", title="              🌡️ Evolución de la temperatura durante el día")
fig1.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    font=dict(color='white'),
    title_font=dict(color='white'),
    legend=dict(font=dict(color='white')),
    xaxis=dict(
        title='Hora',
        color='white',
        tickformat="%H:%M",  # formato de hora
        gridcolor='rgba(255, 255, 255, 0.2)'
    ),
    yaxis=dict(
        title='Temperatura (°C)',
        color='white',
        gridcolor='rgba(255, 255, 255, 0.4)'
    ),
    autosize=True,
    margin=dict(l=20, r=20, t=40, b=40)
)

fig2 = px.line(df, x="hour", y="humidity", title="              🌡️ Evolución de la humedad durante el día")

# Estilo personalizado
fig2.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    font=dict(color='white'),
    title_font=dict(color='white'),
    legend=dict(font=dict(color='white')),
    xaxis=dict(
        title='Hora',
        color='white',
        tickformat="%H:%M",  # formato de hora
        gridcolor='rgba(255, 255, 255, 0.2)'
    ),
    yaxis=dict(
        title='Humedad (%)',
        color='white',
        gridcolor='rgba(255, 255, 255, 0.4)'
    ),
    autosize=True,
    margin=dict(l=20, r=20, t=40, b=40)
)

fig3 = px.line(df, x="hour", y="precipitation", title="              🌡️ Evolución de la lluvia durante el día")
fig3.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    font=dict(color='white'),
    title_font=dict(color='white'),
    legend=dict(font=dict(color='white')),
    xaxis=dict(
        title='Hora',
        color='white',
        tickformat="%H:%M",  # formato de hora
        gridcolor='rgba(255, 255, 255, 0.2)'
    ),
    yaxis=dict(
        title='Precipitación (L/m2)',
        color='white',
        gridcolor='rgba(255, 255, 255, 0.4)'
    ),
    autosize=True,
    margin=dict(l=20, r=20, t=40, b=40)
)

tab1, tab2, tab3 = st.tabs(["Temperatura", "Humedad", "Precipitación"])

with tab1:
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.plotly_chart(fig3, use_container_width=True)


with st.expander("🗂️ Ver datos detallados de mañana"):
    st.dataframe(df)