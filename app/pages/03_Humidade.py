import streamlit as st
import pandas as pd
import plotly.express as px
from utils.filters import *
from utils.df_functions import *
from utils.graphics import *

st.set_page_config(layout="wide", page_title="Morriña en Galicia - Humedad", page_icon="🌫️")
cargar_css("app/static/styles.css")

# Cargar tu dataframe (esto puedes adaptarlo si usas session_state o carga desde archivo)
# Cargar datos
if "df_climatico" not in st.session_state:
    localizacion, localizacion_var = local(page_name='humedad')
    st.session_state["df_climatico"] = cargar_df(localizacion_var, localidades)
else:
    localizacion, localizacion_var = local(page_name='humedad')
# Filtros principales
df = st.session_state["df_climatico"]

if df is None:
    st.warning("No se ha encontrado el DataFrame. Asegúrate de cargar los datos primero en la página principal.")
    st.stop()

st.markdown("<br>", unsafe_allow_html=True)
st.title(f"🌫️ Humidade Relativa en Galicia")

df_filtrado, año, mes = aplicar_filtros(df)
df_grouped, df_conteo = df_grouped_conteo(df_filtrado)

################# MÉTRICAS PARA TODA GALICIA
# CIUDAD MÁS HUMEDA
# CIUDAD MÁS SECA
# MES MÁS HUMEDO
# MES MÁS SECO
# DÍA MÁS HUMEDO
# DÍA MÁS SECO

df_gal = df_galicia()
df_kpi = df_gal.groupby("ciudad")


# Ciudad menos humeda
ciudad_menos_humeda, valor_menos_humedo = obtiene_minimo(df_kpi, 'humedad')

# Ciudad más humeda
ciudad_mas_humeda, valor_mas_humedo = obtiene_maximo(df_kpi, 'humedad')


df_temp = df_gal.copy()
# Crear una columna 'mes' en formato año-mes
df_temp["mes"] = df_temp["fecha"].dt.to_period("M")
# Agrupar por mes y sumar la humedad
humedad_por_mes = df_temp.drop('ciudad', axis = 1).groupby("mes")["humedad"].sum()
# Obtener el mes con más humedad
mes_mas_humedado = humedad_por_mes.idxmax()
humedad_total_mes = humedad_por_mes.max()


# Mes más frío (mínima humedad media mensual)
df_temp["mes"] = df_temp["fecha"].dt.to_period("M")

# Mes más humedo, mes menos humedo
min_mes_hum, max_mes_hum = max_min_func(df_temp, 'mes', 'humedad', 'median')
mes_mas_humedo, mes_mas_humedo_valor = max_mes_hum
mes_menos_humedo, mes_menos_humedo_valor = min_mes_hum

# Dia más humedo, dia menos humedo
min_hum, max_hum = max_min_func(df_gal, 'fecha', 'humedad', 'median')
fecha_min, valor_min = min_hum
fecha_max, valor_max = max_hum

# Mostrar métricas
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("💧 Ciudad más húmeda", ciudad_mas_humeda, f"{valor_mas_humedo:.2f} %", delta_color="off")
    st.metric("🌵 Ciudad menos húmeda", ciudad_menos_humeda, f"{valor_menos_humedo:.2f} %", delta_color="off")

with col2:
    st.metric("📆🔼 Día más húmedo", pd.to_datetime(fecha_max).strftime("%d %b %Y"), f"{valor_max:.2f} %", delta_color="off")
    st.metric("📆🔽 Día menos húmedo", pd.to_datetime(fecha_min).strftime("%d %b %Y"), f"{valor_min:.2f} %", delta_color="off")
with col3:
    st.metric("📅🔼 Mes más húmedo", str(mes_mas_humedo.strftime("%B %Y")), f"{mes_mas_humedo_valor:.2f} %", delta_color="off")
    st.metric("📅🔽 Mes menos húmedo", str(mes_menos_humedo.strftime("%B %Y")), f"{mes_menos_humedo_valor:.2f} %", delta_color="off")

with st.expander("📊 Análisis KPIs de Humidade en Galicia"):
    st.markdown("""
    Estos primeros KPIs son estáticos en base a Galicia, tomando en cuenta todas las ciudades. Donde podemos observar la primera fila relacionado a lo más húmedo y la segunda fila relacionado a lo menos húmedo.  
    Por un lado vemos que la ciudad más húmeda es Coruña y la menos húmeda es Ourense, esto tiene todo el sentido en base a la ubicación geográfica de Coruña y de Ourense, al una estar tan cerca del mar es más húmeda y la otra al estar tan lejos es menos húmeda. 
    
    Luego de estos tenemos los días más húmedos que concuerdan con los meses más humedos, estos equivalen a Otoño (temporada más húmeda) y el inicio de la primavera (temporada menos húmeda). Podría ser raro que Abril sea el mes con menos humedad, ya que no es el mes más seco, pero al estar en esta transición de invierno a primavera suelen darse climas con poca humedad, se está saliendo de un inverno posiblemente lluvioso como es el de las tierras gallegas y no han comenzado las lluvias convectivas más frecuentes de primavera/verano, lo que favorece a esta baja humedad.
    
    Estos KPIs referentes a fecha son difíciles de explicar ya que vienen dados por la estacionalidad y complementados por todo el entorno de la región de Galicia, tomando en cuenta todo el ambiente de la Peninsula, la cordillera y el Atlántico, por lo que para dar conclusiones con mayor propiedad se deberían tomar todas estas variables en cuenta. Por eso, esto es simplemente una pequeña explicación y razonamiento propio sobre los datos mostrados.
    """)

############################################################################
st.markdown("---")
st.subheader(f"📍 Localización: {localizacion}")
# BARPLOT TEMPERATURA: VARIABLE CATEGÓRICA
# BARPLOT CATEGORICO
categorias = {'Seco 🌵 (<50%)':50, 
              'Moderado 🌤️ (50–75%)':75,
              'Húmedo 💧 (>75%)':100}
colores = {
    'Seco 🌵 (<50%)': 'rgb(204, 204, 204)',  # Gris claro para baja humedad
    'Moderado 🌤️ (50–75%)': 'rgb(102, 153, 255)',  # Azul claro para humedad moderada
    'Húmedo 💧 (>75%)': 'rgb(7, 121, 197)' # Azul fuerte para alta humedad
}

df_hum_cat = df_categorico(df_filtrado, 'humedad', categorias)
fig_bar_hum = fig_bar_humedad(df_hum_cat, colores)
#st.plotly_chart(fig_bar_hum, use_container_width=True)

col1, col2 = st.columns([2, 1])  # 2 partes y 1 parte → 66% y 33%

with col1:
    st.plotly_chart(fig_bar_hum, use_container_width=True)

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>🔼 Humedad máxima</h5><h2 >{} %</h2></div>".format(round(df_grouped['humedad'].max(), 2)), unsafe_allow_html=True)
    st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>➖ Humedad promedio</h5><h2 >{} %</h2></div>".format(round(df_grouped['humedad'].mean(), 2)), unsafe_allow_html=True)
    st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>🔽 Humedad mínima</h5><h2 >{:.1f} %</h2></div>".format(df_grouped['humedad'].min()), unsafe_allow_html=True)

with st.expander("📊 Explicación KPIs de Humidade en {localizacion}"):
    st.markdown("""
    Para la humedad vemos primero una gráfica de barras donde se creó una variable categórica para dividir el rango de humedad, es destacable mencionar que estas divisiones no son muy propias en una literatura, ya que un clima "seco" no llega hasta 50% de humedad, pero al estar tratando de Galicia, una región muy húmeda, se tuvo que alterar para poder tener algunos valores dentro de esta variable.
    El comportamiento es igual para todas las ciudades y obviamente la región en general, predominando un clima bastante húmedo. Varia la cuenta de los días dependiendo de la ciudad, pero siempre es más o menos similar.
    
    Por otra parte, los KPIs son explicitos. Aquí lo más relevante es que los valores de humedad "promedio" entran dentro de un clima húmedo, reforzando así el tipo de clima presente en las tierras del noroeste de España. Lo mismo se puede visualizar en las otras dos, donde el mínimo entra por muy poco como clima "seco".
    """)

# LINEA DE HUMEDAD MENSUAL
fig_hume_mes = plot_hum_mes(df_filtrado, localizacion)
st.plotly_chart(fig_hume_mes, use_container_width=True)

# DISTRIBUCIÓN DE HUMEDAD (HISTOGRAMA O UN KDE): Te dice en qué rango de humedad se mueven la mayoría de los días
fig_humidity_kde_clean = plot_humidity_kde_line(df_filtrado, localizacion)
st.plotly_chart(fig_humidity_kde_clean, use_container_width=True)

# LINEA DE HUMEDAD DIARIA: Muestra la evolución temporal y diferencias entre ciudades
fig_humidity_line = plot_humidity_line(df_filtrado, localizacion)
st.plotly_chart(fig_humidity_line, use_container_width=True)

with st.expander("📊 Análisis de gráficas de Humidade en {localizacion}"):
    st.markdown("""
    Aquí se presentan tres gráficas de lineas, un poco diferentes entre ellas. Dos son similares, donde representan el valor medio de humedad, en una mensualmente y el otro de forma diario. Esto se realizó simplemente para ver en detalle alguna parte del tiempo de ser necesario. Pero las conclusiones se generan a partir de la humedad mensual.
    Podemos ver en esta que los valores de humedad tanto para Coruña como para Ourense son ajenos al resto de ciudades gallegas. Por una parte Coruña se comporta muy húmeda en comparación al resto en la mayoría del tiempo,
    mientras que Ourense todo lo contrario, normalmente suele bajar mucho la Humedad a lo largo del verano. 
    Otra cosa a destacar es un "pico en bajada", este se encuentra entre Enero y Abril y se presenta básicamente en todas las ciudades. En el 2023 estuvo en enero y se repitió en menor cantidad en Mayo, para el 2024 fue en Abril y para el 2025 se nota ya en Marzo.
    
    Luego tenemos la distribución suavizada, esto sería como ver un histograma del porcentaje de humedad en la totalidad de los datos. Aquí podemos ver donde se concentran la mayor cantidad de datos de cada ciudad. Lo más llamativo sigue siendo Ourense y Coruña. Donde Ourense tiene una distribución bimodal, a los 60 y 80%, al igual que Coruña, pero esta a los a los 80% en menor cantidad y a los 95% el otro pico.
    """)

# MAPA DE CALOR (HEATMAP): Muy visual para ver tendencias, anomalías o días con humedad alta/baja
if localizacion_var == "galicia":
    fig_humidity_heatmap = plot_humidity_heatmap(df_filtrado, localizacion)
    st.plotly_chart(fig_humidity_heatmap, use_container_width=True)
    
with st.expander("📊 Análisis de gráficas de Humidade en {localizacion}"):
    st.markdown("""
    Esta última gráfica sólo está presente si estamos viendo a Galicia, ya que presenta a todas las ciudades. Esta muestra el procentaje de humedad por ciudad a lo largo del tiempo, asemejando un heatmap, pero entre fecha y ciudad.
    Esto representa la variabilidad tanto en tiempo como en ciudad. Donde se puede observar una gran mancha azul entre Octubre y Enero, pero en Coruña del 2023 fue bastante extensa, en más de medio año, esto puede significar que quizás fue algo anómalo para la ciudad.
    Mientras que vemos que Ourense si se nota la estacionalidad, donde a penas pisa Abril se empiezan ver valores blancos (cercanos a 60%) y el resto más tonalidades azules.
    """)