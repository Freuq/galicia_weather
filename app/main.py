import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from utils.filters import aplicar_filtros

def cargar_css(path: str):
    with open(path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Llama a la función
cargar_css("app/static/styles.css")

st.markdown("""
    <style>
    /* Fondo azul oscuro para el contenido principal */
    .block-container {
        background-color: #155ea6;
        color: white;
        padding: 2rem;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Resumen Climático General")
st.subheader("📍 Localización: Santiago de Compostela")
st.markdown("<br>", unsafe_allow_html=True)
# Cargar datos
df = pd.read_csv("data/processed/weather_santiago.csv", parse_dates=["Fecha"])

# Aplicar filtros desde el archivo utils/filters.py
df_filtrado, año, mes = aplicar_filtros(df)

# Lluvia en Santiago
st.markdown(
    "<h3 style='text-align: center;'>🌧️ Lluvia en Santiago</h3>",
    unsafe_allow_html=True
)
# Mostrar algunos KPIs simples
col1, col2, col3 = st.columns(3)

# Centrar tanto títulos como métricas
col1.markdown("<div style='text-align: center;'><h5 style='padding-bottom: 0.1px;';'>Días totales</h5><h2 >{}</h2></div>".format(len(df_filtrado)), unsafe_allow_html=True)
col2.markdown("<div style='text-align: center;'><h5 style='padding-bottom: 0.1px;';'>Días con lluvia</h5><h2 >{}</h2></div>".format((df_filtrado["lluvia"] > 0).sum()), unsafe_allow_html=True)
col3.markdown("<div style='text-align: center;'><h5 style='padding-bottom: 0.1px;';'>Lluvia total (L/m2)</h5><h2 >{:.1f}</h2></div>".format(df_filtrado['lluvia'].sum()), unsafe_allow_html=True)



# Lluvia diaria
fig_rain = px.bar(df_filtrado, x="Fecha", y="lluvia", title="         Precipitación diaria en Santiago de Compostela")
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


st.markdown(
    "<h3 style='text-align: center;'>🌡️ Temperatura en Santiago</h3>",
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)
col1.markdown("<div style='text-align: center;'><h5 style='padding-bottom: 0.1px;';'>Promedio (ºC)</h5><h2 >{}</h2></div>".format(round(df_filtrado['temperatura_media'].mean(), 2)), unsafe_allow_html=True)
col2.markdown("<div style='text-align: center;'><h5 style='padding-bottom: 0.1px;';'>T máxima (ºC)</h5><h2 >{}</h2></div>".format(df_filtrado['temperatura_media'].max()), unsafe_allow_html=True)
col3.markdown("<div style='text-align: center;'><h5 style='padding-bottom: 0.1px;';'>T mínima (ºC)</h5><h2 >{:.1f}</h2></div>".format(df_filtrado['temperatura_media'].min()), unsafe_allow_html=True)

# Temperatura diaria

fig_temp = px.line(df_filtrado, x="Fecha", y="temperatura_media", title="Temperatura media diaria en Santiago")
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

# Visualización: lluvia y temperatura
fig = px.line(df_filtrado, x="Fecha", y=["lluvia", "temperatura_media"], title="Lluvia y Temperatura diarias")
fig.update_layout(yaxis_title="Valor", legend_title="Variable")
fig.update_xaxes(dtick="M1", tickformat="%b %Y")
fig.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',  # Fondo de la gráfica transparente
    paper_bgcolor='rgba(0, 0, 0, 0)',  # Fondo del paper transparente
    font=dict(color='white'),
    title_font=dict(color='white'),
    legend=dict(font=dict(color='white')),
    xaxis=dict(color='white'),
    yaxis=dict(
        color='white',
        gridcolor='rgba(255, 255, 255, 0.4)'),
    autosize=True,
    margin=dict(l=20, r=20, t=40, b=40)
)

st.plotly_chart(fig, use_container_width=True)