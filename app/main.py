import streamlit as st
from utils.filters import *
from utils.graphics import *
from utils.df_functions import *

# Diseño de la página
st.set_page_config(layout="wide", page_title="Morriña en Galicia", page_icon="⛅")
cargar_css("app/static/styles.css")
# Configuración de la página

st.title("⛅Morriña en Galicia")

localidades = {
    "galicia": "Galicia",
    "santiago": "Santiago de Compostela",
    "coruna": "Coruña",
    "lugo": "Lugo",
    "ourense": "Ourense",
    "pontevedra": "Pontevedra",
    "vigo": "Vigo"}

# Guardar la localización previa (si existía)
localizacion_anterior = st.session_state.get("localizacion_anterior", None)

# Obtener localización actual
localizacion, localizacion_var = local(page_name="main")

# Si no existe el df o ha cambiado la ciudad, cargar nuevo df
if ("df_climatico" not in st.session_state) or (localizacion != localizacion_anterior):
    st.session_state["df_climatico"] = cargar_df(localizacion_var, localidades)
    st.session_state["localizacion_anterior"] = localizacion  # actualizar

df = st.session_state["df_climatico"]



df = st.session_state["df_climatico"]
st.subheader(f"📍 Localización: {localizacion}")

# Aplicar filtros desde el archivo utils/filters.py
df_filtrado, año, mes = aplicar_filtros(df)
#localizacion, localizacion_var = local(page_name='main')
# Cargar datos
#df = cargar_df(localizacion_var, localidades)
#if "df_climatico" not in st.session_state:
#    st.session_state["df_climatico"] = df

# MAPA
map_html = map_local(localizacion_var)

# Forzar estilo en div padre e iframe
st.components.v1.html(f"""
    <div style="width: 100%; height: 520px; border-radius: 15px; overflow: hidden; border: none;">
        <iframe srcdoc='{map_html}' style="width: 100%; height: 100%; border: none;"></iframe>
    </div>
""", height=520)

# GENERACIÓN DE DF_GROUPED (VALORES AGRUPADOS PARA GALICIA) Y DF_CONTEO (NRO DE DÍAS CON LLUVIA Y SIN LLUVIA)
df_grouped, df_conteo = df_grouped_conteo(df_filtrado)
st.markdown("---")
####################################################### PRECIPITACIÓN #######################################################
st.markdown(
    f"<h2 style='text-align: center;'>☔<a href='/Choiva' target='_self' style='color: #ffffff;'>Choiva en {localizacion}</a></h2>",
    unsafe_allow_html=True
)

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
        st.markdown("<h4 style='text-align: center;'>Lluvia (L/m²)</h4>", unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Total</h5><h2 >{}</h2></div>".format(int(df_grouped['precipitacion'].sum())), unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Promedio</h5><h2 >{}</h2></div>".format(round(df_grouped['precipitacion'].mean(), 2)), unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Maximo</h5><h2 >{}</h2></div>".format((df_grouped["precipitacion"]).max()), unsafe_allow_html=True)
        
    with subcol3:
        st.markdown("<h4 style='text-align: center;'>En meses</h4>", unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Meses totales</h5><h2 >{}</h2></div>".format(total_meses), unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Más lluvioso</h5><h2 >{}</h2></div>".format(mes_mas_lluvioso), unsafe_allow_html=True)
        st.markdown("<div class='custom-container'><h5 style='padding-bottom: 0.1px;';'>Menos lluvioso</h5><h2 >{}</h2></div>".format(mes_menos_lluvioso), unsafe_allow_html=True)
with st.expander("📊 Análisis de Choiva en Galicia"):
    st.markdown("""
    El gráfico de pe a la izquierda representa la cantidad de días sin lluvia y con lluvia que hay en dicha Población. Para todas las ciudades por individual hay más días SIN lluvia,
    pero al ver toda Galicia sí hay más días con lluvia (469 días). Si consideramos sólo las ciudades des mayor cantidad de días con lluvia a menor, sería de la siguente forma:
    Santiago de Compostela > Coruña > Lugo > Pontevedra > Vigo > Ourense.
    
    Por otra parte, las métricas señaladas del lado derecho expresan diferentes puntos de valor. De los cuales podemos destacar que los meses más lluviosos y menos lluviosos se suelen repetir en casi todas las ciudades.
    A excepción de Pontevedra y Vigo, donde su mes más lluvioso es Octubre y el menos lluvioso es Agosto y Julio, respectivamente.
    
    Para más detalle ir a la sección de lluvia.
    """)

st.markdown("---")
################################################### TEMPERATURA #######################################################
st.markdown(
    f"<h2 style='text-align: center;'>🌡️<a href='/Temperatura' target='_self' style='color: #ffffff;'>Temperatura en {localizacion}</a></h2>",
    unsafe_allow_html=True
)

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

with st.expander("📊 Análisis de Temperatura en Galicia"):
    st.markdown("""
    Por el lado del Barplot se puede observar una clasificación los días para la localización que se esté observando, como tendencia tenemos que la mayoría de los días se califican como días templados🌤️ (10–20°C).
    La ciudad que menos días Templados tiene es Ourense, esto significa que es la ciudad con mayor variabilidad de temperatura, ya que apesar de que la distribución se mantiene (Templado > Cálido y Frío),
    tiene una diferencia entre ellas mucho menor a comparación de los otros sitios.
    
    Además se observan la temperatura máxima y mínima, ambas históricos. Estos resultados para Galicia se obtuvieron tomando en cuenta el promedio de las seis ciudades, siendo así los máximos y mínimos de ciudades en particular menores que en toda la región.
    La menor temperatura es en Lugo (0.56 ºC) y la mayor temperatura en Ourense (31.0 ºC).
    
    Para más detalle ir a la sección de temperatura.
    """)

st.markdown("---")
########################################### HUMEDAD RELATIVA #######################################################
st.markdown(
    f"<h2 style='text-align: center;'>🌫️<a href='/Humidade' target='_self' style='color: #ffffff;'>Humidade Relativa en {localizacion}</a></h2>",
    unsafe_allow_html=True
)

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

with st.expander("📊 Análisis de Humidade en Galicia"):
    st.markdown("""
    Aquí se presenta una clasificación de Humedad Relativa, es impresionante observar como la humedad es un parámetro que siempre está muy presente en el clima gallego,
    Llegando a tener un promedio (75.43 %) para la zona que ya es considerado húmedo (>75%). Estando todas ellas por menos de diez días Secos en los datos presentados (2023 a 2025)
    
    Estos datos hacen ver lo representativa que llega a ser la humedad para Galicia, que inclusive en días de más calor, puede haber sensaciones de más frío o inclusive "bochorno".
    
    Para más detalle ir a la sección de temperatura.
    """)
################################## DF ####################################
st.markdown("---")
st.markdown(
    f"<h2 style='text-align: center;'>DataFrame de {localizacion}</h2>",
    unsafe_allow_html=True
)
with st.expander("🗂️ Ver datos utilizados"):
    st.dataframe(df_filtrado)
####################################### COMPARATIVAS #######################################################
#st.markdown("---")
#st.markdown(
#    f"<h2 style='text-align: center;'>Temperatura vs Humidade en {localizacion}</h2>",
#    unsafe_allow_html=True
#)

# SCATTER PLOT ENTRE TEMP Y HUMEDAD: Para ver correlaciones o agrupaciones
#fig_temp_vs_humidity = plot_temp_vs_humidity(df_filtrado, localizacion)
#st.plotly_chart(fig_temp_vs_humidity, use_container_width=True)

# LINEA CON DOBLE EJE Y: Útil para ver cómo cambian juntas en el tiempo
#fig_temp_humidity = plot_temp_humidity_dual_axis(df_grouped, localizacion)
#st.plotly_chart(fig_temp_humidity, use_container_width=True)
#with st.expander("📊 Proximo análisis"):
#    st.markdown("""
#    Esta sección será dedicada en un futuro a la relación entre las variables Temperatura y Humedad, para poder explicar y ver la presencia de días de "bochorno" en Galicia y ese frío que "se mete por los huesos"
#    """)


