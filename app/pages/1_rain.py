import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🌧️ Análisis de Lluvia")

def cargar_css(path: str):
    with open(path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Llama a la función
cargar_css("app/static/styles.css")

# Cargar datos
df = pd.read_csv("data/processed/weather_santiago.csv", parse_dates=["Fecha"])

# Pie chart días con y sin lluvia
df["llovio"] = df["lluvia"] > 0
conteo = df["llovio"].value_counts().rename({True: "Día con lluvia", False: "Día sin lluvia"}).reset_index()
conteo.columns = ["Tipo de día", "Cantidad"]

fig_pie = px.pie(conteo, names="Tipo de día", values="Cantidad", hole=0.4)
fig_pie.update_traces(textinfo="percent+label")
st.plotly_chart(fig_pie, use_container_width=True)

# Visualización: lluvia diaria
fig = px.bar(df, x="Fecha", y="lluvia", title="Lluvia diaria (mm)")
fig.update_xaxes(dtick="M1", tickformat="%b %Y")
st.plotly_chart(fig, use_container_width=True)


