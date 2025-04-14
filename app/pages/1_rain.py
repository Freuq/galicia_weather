import streamlit as st
import pandas as pd
import plotly.express as px
st.markdown("<br>", unsafe_allow_html=True)
st.title("🌧️ Análisis de Lluvia")

def cargar_css(path: str):
    with open(path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Llama a la función
cargar_css("app/static/styles.css")

# Cargar datos
df = pd.read_csv("data/processed/weather_santiago.csv", parse_dates=["fecha"])

# Pie chart días con y sin lluvia
df["llovio"] = df["precipitacion"] > 0
conteo = df["llovio"].value_counts().rename({True: "Días con lluvia", False: "Días sin lluvia"}).reset_index()
conteo.columns = ["Tipo de día", "Cantidad"]

fig_pie = px.pie(conteo, title="         Cantidad y porcentaje de días con y sin lluvia en Santiago", names="Tipo de día", values="Cantidad", hole=0.4)
fig_pie.update_traces(
    textinfo="percent+label+value", 
    marker=dict(
        colors=['#4FC3F7', '#FFEB3B']))
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
st.plotly_chart(fig_pie, use_container_width=True)

# Lluvia diaria
fig_rain = px.bar(df, x="fecha", y="precipitacion", title="         Precipitación diaria en Santiago de Compostela")
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


