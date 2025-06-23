import streamlit as st
import pandas as pd
import plotly.express as px
from utils.filters import *
from utils.df_functions import *
from utils.graphics import *

st.set_page_config(layout="wide", page_title="Morriña en Galicia - Lluvia", page_icon="🌧️")
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
st.title(f"☔ Choiva en Galicia")

df_filtrado, año, mes = aplicar_filtros(df)
df_grouped, df_conteo = df_grouped_conteo(df_filtrado) # df_grouped para los valores de localización y df_conteo para el pie_plot

################# MÉTRICAS PARA TODA GALICIA
# CIUDAD CON MÁS DÍAS LLOVIENDO, CIUDAD CON MÁS LLUVIA MEDIA
# CIUDAD CON MENOS DÍAS LLOVIENDO, CIUDAD CON MÁS MENOS LLUVIA MEDIA
# DÍA MÁS LLUVIOSO
# Utilizamos el df original para toda Galicia
df_gal = df.copy()
# Agrupamos por ciudad
df_kpi = df_gal.groupby("ciudad")

# Ciudad con más y menos días de lluvia (> 0 mm)
dias_lluvia = df_gal[df_gal["precipitacion"] > 0].groupby("ciudad").size()
ciudad_mas_dias_lluvia = dias_lluvia.idxmax()
ciudad_menos_dias_lluvia = dias_lluvia.idxmin()

# Ciudad con mayor y menor precipitación media
precipitacion_media = df_kpi["precipitacion"].mean()
ciudad_mas_lluvia_media = precipitacion_media.idxmax()
ciudad_menos_lluvia_media = precipitacion_media.idxmin()

df_dias = df_gal.drop('ciudad', axis = 1).groupby("fecha")["precipitacion"].sum()

# Día más lluvioso
fecha_mas_lluviosa = df_dias.idxmax()
lluvia_maxima = df_dias.max()

# Asegurarse de que la columna 'fecha' es datetime
df_gal["fecha"] = pd.to_datetime(df_gal["fecha"])
# Crear una columna 'mes' en formato año-mes
df_gal["mes"] = df_gal["fecha"].dt.to_period("M")
# Agrupar por mes y sumar la precipitación
precipitacion_por_mes = df_gal.drop('ciudad', axis = 1).groupby("mes")["precipitacion"].sum()
# Obtener el mes con más precipitación
mes_mas_lluvioso = precipitacion_por_mes.idxmax()
lluvia_total_mes = precipitacion_por_mes.max()

# Mostrar métricas
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🌧️ Ciudad con más días de lluvia", ciudad_mas_dias_lluvia, f"{dias_lluvia.max()} días", delta_color="off")
    st.metric("🌤️ Ciudad con menos días de lluvia", ciudad_menos_dias_lluvia, f"{dias_lluvia.min()} días", delta_color="off")
with col2:
    st.metric("🌂 Ciudad con más lluvia media", ciudad_mas_lluvia_media, f"{precipitacion_media.max():.2f} L/m²", delta_color="off")
    st.metric("🌵 Ciudad con menos lluvia media", ciudad_menos_lluvia_media, f"{precipitacion_media.min():.2f} L/m²", delta_color="off")
with col3:
    st.metric("📆 Día más lluvioso", pd.to_datetime(fecha_mas_lluviosa).strftime("%d %b %Y"), f"{lluvia_maxima:.2f} L/m²", delta_color="off")
    st.metric("📅 Mes más lluvioso", mes_mas_lluvioso.strftime("%B %Y"), f"{lluvia_total_mes:.2f} L/m²", delta_color="off")

with st.expander("📊 Análisis KPIs de Choiva en Galicia"):
    st.markdown("""
    Estos primeros KPIs son estáticos en base a Galicia, tomando en cuenta todas las ciudades. Donde podemos observar la primera fila relacionado a lo más lluvioso y la segunda fila relacionado a lo menos lluvioso.  
    Por un lado vemos que Santiago de Compostela es la ciudad donde más días llueve y donde más lluvia media hay, mientras que Ourense es la ciudad donde menos lluvia, tanto en cantidad de días como en lluvia media.
    
    Por último vemos en la última columna el día más lluvioso de todo el dataset (26 de Octubre 2023), el cual fue el mes donde más llovio en todos los datos que se tiene (Octubre 2023) junto con sus respectivos valores en L/m², sólo el día 26 llovió 
    """)
st.markdown("---")

######### METRICAS UTILIZANDO FILTROS 
st.subheader(f"📍 Localización: {localizacion}")
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
        st.markdown("<h4 style='text-align: center;'>Lluvia (L/m2)</h4>", unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Total</h5><h2 >{}</h2></div>".format(int(df_grouped['precipitacion'].sum())), unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Promedio</h5><h2 >{}</h2></div>".format(round(df_grouped['precipitacion'].mean(), 2)), unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Maximo</h5><h2 >{}</h2></div>".format((df_grouped["precipitacion"]).max()), unsafe_allow_html=True)
        
    with subcol3:
        st.markdown("<h4 style='text-align: center;'>En meses</h4>", unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Meses totales</h5><h2 >{}</h2></div>".format(total_meses), unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Más lluvioso</h5><h2 >{}</h2></div>".format(mes_mas_lluvioso), unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Menos lluvioso</h5><h2 >{}</h2></div>".format(mes_menos_lluvioso), unsafe_allow_html=True)

with st.expander(f"📊 Explicación de KPIs de Choiva en {localizacion}"):
    st.markdown(f"""
    En esta parte se plantean ya KPIs en base a filtros aplicados en clima, año y mes. Por lo que este análisis se hace automático.
    
    Podemos observar primero una gráfica de pie que representa los días con lluvia y sin lluvia, donde podemos ver su total de "{df_conteo["Tipo de día"][1]}" igual a {df_conteo["Cantidad"][1]} en color amarillo, mientras que los "{df_conteo["Tipo de día"][0]}"
    fueron un total de {df_conteo["Cantidad"][0]} en color azul. Hay que tomar en cuenta que esto equivale para cualquier lluvia, no importa la cantidad que fue.  
    
    Luego tenemos todos los KPIs, desde la división en días, en lluvia y por meses. De esta sección lo más relevante es los meses más y menos lluviosos, estos en la mayoría de los casos es extremo, ya que hay medio año entre ellos, lo que representa el ciclo climático anual.
    """)

# lluvia mensual
fig_rain_monthly = plot_lluvia_mes(df_filtrado, localizacion)
st.plotly_chart(fig_rain_monthly)

# Lluvia diaria
fig_rain = plot_lluvia_bar(df_filtrado, localizacion)
st.plotly_chart(fig_rain, use_container_width=True)

with st.expander(f"📊 Análisis de gráficas de Choiva en {localizacion}"):
    st.markdown(f"""
    Estas dos gráficas presentan similitudes, ya que hablamos de la misma medida pero con un cambio de granularidad. En una es representado a nivel mensual, mientras que la otra a nivel diario. Si se utiliza la variable Galicia estas son de barras apiladas, para que se pueda observar la representación de cada ciudad en la gráfica.
    A groso modo podemos observar que el mes donde más llovio fue en Oct del 2023 y a lo largo de todos los meses se observa que los dos meses donde más suele llover es en Enero y en Octubre. Por su contraparte tenemos a Julio y Agosto, que son en los que menos suele llover, con una que otra excepción.
    
    Al ver este gráfico en días puede ser un poco más confuso, pero es importante para visualizar si las conclusiones dadas en meses no son por días sueltos que cambian la tendencia. Una de las características más llamativas de las gráficas de Plotly es que son interactivas y permiten hacer zoom si se selecciona una parte de la gráfica.
    Esto lo usamos para acercarnos a las zonas de interés. Y se puede destacar que la tendencia suele dividirse en dos meses, ya que por ejemplo en Oct 2023, es cierto que Octubre es el mes con más lluvia, pero muchos de estos días siguen cayendo en Noviembre, sólo que a menor densidad de lluvia. Tanto así que vemos que para los primeros 10 días del mes siquiera hubo lluvia.
    
    La tendencia de lluvia se repite en Octubre del 2024 que es cierto que no fue el mes con más lluvia, pero se puede observar que sí es el mes con más días juntos de lluvia. Lo que nos lleva a decir que la temporada Octubre-Noviembre es posible en la que más suele llover en el suelo gallego, obviamente en base a esta pequeña muestra de dos años y medio.
    
    Este gráfico se podría desmenusar más a fondo, pero es cierto que para visualizar patrones con seguridad habría que obtener una cantidad de datos histórica mayor.
    """)