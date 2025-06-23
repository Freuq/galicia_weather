import streamlit as st
import pandas as pd
import plotly.express as px
from utils.filters import *
from utils.df_functions import *
from utils.graphics import *

st.set_page_config(layout="wide", page_title="Morriña en Galicia - Temperatura", page_icon="🌡️")
cargar_css("app/static/styles.css")

# Cargar tu dataframe (esto puedes adaptarlo si usas session_state o carga desde archivo)
# Cargar datos
if "df_climatico" not in st.session_state:
    localizacion, localizacion_var = local(page_name='temperature')
    st.session_state["df_climatico"] = cargar_df(localizacion_var, localidades)
else:
    localizacion, localizacion_var = local(page_name='temperature')
# Filtros principales
df = st.session_state["df_climatico"]

if df is None:
    st.warning("No se ha encontrado el DataFrame. Asegúrate de cargar los datos primero en la página principal.")
    st.stop()

st.markdown("<br>", unsafe_allow_html=True)
st.title(f"🌡️ Temperatura en Galicia")

df_filtrado, año, mes = aplicar_filtros(df)
df_grouped, df_conteo = df_grouped_conteo(df_filtrado)

################# MÉTRICAS PARA TODA GALICIA
# CIUDAD MÁS FRÍA
# CIUDAD MÁS CÁLIDA
# MES MÁS FRÍO
# MES MÁS CÁLIDO
# DÍA MÁS FRÍO
# DÍA MÁS CÁLIDO
# Agrupamos por ciudad
# Asegurarse de que la columna 'fecha' es datetime
df_gal = df.copy()
df_gal["mes"] = df_gal["fecha"].dt.to_period("M")
# Agrupamos por ciudad
df_kpi = df_gal.groupby("ciudad")

# Ciudad menos humeda
ciudad_menos_temp, valor_menos_temp = obtiene_minimo(df_kpi, 'temperatura')

# Ciudad más humeda
ciudad_mas_temp, valor_mas_temp = obtiene_maximo(df_kpi, 'temperatura')

# Ciudad con pico más frío (mínima temperatura)
ciudad_mas_fria_pico = df_kpi["temperatura"].min().idxmin()
pico_mas_frio = df_kpi["temperatura"].min().min()

# Ciudad con pico más cálido (máxima temperatura)
ciudad_mas_calida_pico = df_kpi["temperatura"].max().idxmax()
pico_mas_calido = df_kpi["temperatura"].max().max()

# Mes menor temp, mes mayor temp
mes_menor_temp, mes_mayor_temp = max_min_func(df_gal, 'mes', 'temperatura', 'median')
mes_menor_temp_nombre, mes_menor_temp_valor = mes_menor_temp
mes_mayor_temp_nombre, mes_mayor_temp_valor = mes_mayor_temp

# Dia menor temp, dia mayor temp
min_temp, max_temp = max_min_func(df_gal, "fecha", 'temperatura', 'median')
fecha_min, valor_min = min_temp
fecha_max, valor_max = max_temp


# Mostrar métricas
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("❄️ Ciudad más fría", ciudad_menos_temp, f"{valor_menos_temp:.2f} °C", delta_color="off")
    st.metric("🌞 Ciudad más calurosa", ciudad_mas_temp, f"{valor_mas_temp:.2f} °C", delta_color="off")
with col2:
    st.metric("❄️ Ciudad con pico más frío", ciudad_mas_fria_pico, f"{pico_mas_frio:.2f} °C", delta_color="off")
    st.metric("🌞 Ciudad con pico más caluroso", ciudad_mas_calida_pico, f"{pico_mas_calido:.2f} °C", delta_color="off")
with col3:
    st.metric("📆🧊 Día más frío", pd.to_datetime(fecha_min).strftime("%d %b %Y"), f"{valor_min:.2f} °C", delta_color="off")
    st.metric("📆🔥 Día más caluroso", pd.to_datetime(fecha_max).strftime("%d %b %Y"), f"{valor_max:.2f} °C", delta_color="off")
with col4:
    st.metric("📅🌬️ Mes más frío", str(mes_menor_temp_nombre.strftime("%B %Y")), f"{mes_menor_temp_valor:.2f} °C", delta_color="off")
    st.metric("📅🌞 Mes más cálido", str(mes_mayor_temp_nombre.strftime("%B %Y")), f"{mes_mayor_temp_valor:.2f} °C", delta_color="off")

with st.expander("📊 Análisis KPIs de Temperatura en Galicia"):
    st.markdown("""
    Estos primeros KPIs son estáticos en base a Galicia, tomando en cuenta todas las ciudades. Donde podemos observar la primera fila relacionado a lo más frío y la segunda fila relacionado a lo más caluroso.  
    Por un lado vemos que Lugo es la ciudad donde más frío hace y donde está el pico más frío a casi 0 grados, mientras que Ourense es la con el pico más caluroso y Vigo la ciudad más calurosa. Es común que los climas de límite, tanto frío como caliente, estén lejos del mar. En esta comunidad autónoma en particular puede que no haya temperaturas tan extremas como en otras partes de España, esto tiene que ver con la cantidad de humedad, vegetación y masa forestal.
    Aunque aquí hay algo que da curiosidad, que si esto es cierto, ¿por qué Vigo tiene mayor temperatura media anual que Ourense?, lo cierto es que están bastante cerca en media, pero siempre se ha hablado que Vigo posee un "microclima", hay varios estudios que intentan explicar esto, pero a grandes rasgos podemos decir que la influencia del Atlántico da inviernos más suaves y veranos menso calurosos, esta orientada al sur con menos vientos fríos y tiene una barrera montañosa que intercepta gran parte de nubes cargadas de lluvia.
    La realidad es que no tanto la geomorfología de la zona como la geolocalización ayudan a que Vigo tenga el clima que tiene y se encuentre como la ciudad más "Calurosa" dentro de las gallegas, que de todas formas a nivel Global 16°C es una temperatura medianamente baja. 
    
    Los otros cuatro valores que tenemos representan los días y mese smás fríos y calurosos dentro de galica. Esta es la temperatura media tomando tomando todas las ciudades gallegas para que sea más representativo. Lo fascinante de esto es que se rige tal cual por el ciclo climático, el momento más frío es en invierno (Enero y Febrero) y el más caliente es en verano (Agosto).
    Esto es fascinante porque nos suelen decir que el mundo está cambiando en base al periodo de desglaciación que estamos viviendo teniendo temperaturas más altas, y la contaminacióne está cambiando el ciclo climático, pero aquí vemos que no es del todo cierto y que los picos se siguen manteniendo donde están, las tendencias siguen existiendo y como siempre hay anomalías y excepciones. 
    """)

st.markdown("---")
st.subheader(f"📍 Localización: {localizacion}")
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

with st.expander(f"📊 Explicación de KPIs de Temperatura en {localizacion}"):
    st.markdown(f"""
    En esta parte se plantean ya KPIs en base a filtros aplicados en clima, año y mes. Por lo que este análisis se hace automático.
    
    Podemos observar primero una gráfica de barras que representa la clasificación de los días en base a su temperatura, donde podemos ver el total de días "{df_temp_cat["categoria"][0]}" igual a {df_temp_cat["count"][0]}, el total de días "{df_temp_cat["categoria"][1]}" igual a {df_temp_cat["count"][1]} y el total de días "{df_temp_cat["categoria"][2]}" igual a {df_temp_cat["count"][2]}. 
    Para realizar esta clasificación se tomó un poco los rangos de temperatura habituales para la zona. Esto en toda Galicia se comporta más o menos igual, siendo la categoría Templado la de mayor cantidad en todos los casos, para la segunda y la tercera varía un poco más, donde todas las ciudades lejos del mar (Ourense, Lugo y Santiago de Compostela) tienen más días fríos que cálidos, mientras que las ciudades costeras lo contrario y siendo las que tienen más días como templados también. Esto se explica con facilidad en base al aporte del mar a la regulación de la temperatura, igual que como se mencionó en Vigo antes, es muy difícil que una ciudad costera tenga temperaturas extremas y sobretodo bajas.
    
    Luego tenemos algunos KPIs de interés para cada ciudad si se quiere ver, como la Tmax, Tprom y Tmin. 
    """)

# LINEA DE TEMPERATURA MENSUAL: Muestra la evolución temporal y diferencias entre ciudades POR MES
fig_temp_monthly = plot_temp_mes(df_filtrado, localizacion)
st.plotly_chart(fig_temp_monthly, use_container_width=True)

# BOXPLOT POR MES: Permite ver la dispersión, medianas y outliers por mes
fig_temp_boxplot = plot_temp_boxplot(df_filtrado, localizacion)
st.plotly_chart(fig_temp_boxplot, use_container_width=True)

# LINEA DE TEMPERATURA DIARIA: Muestra la evolución temporal y diferencias entre ciudades
fig_temp_line = plot_temp_line(df_filtrado, localizacion)
st.plotly_chart(fig_temp_line, use_container_width=True)

with st.expander(f"📊 Análisis de gráficas de Temperatura en {localizacion}"):
    st.markdown(f"""
    La primera y tercera gráfica tienen una distribución similar, ya que en ellas simplemente cambia la granularidad. Una va a mes y la otra a día, esto para poder observar las diferencias en días si es necesario.
    Para la segunda gráfica por otra parte tenemos los valores para una gráfica de Box, donde se pueden ver valores anómalos, máximos, medianas y mínimos.
    
    La primera y la tercera de lineas presentan tendencias similares, en los meses calurosos bajas y en los meses fríos suben. Esto No parece muy interesante, pero en la gráfica de Temperatura mensual podemos observar la tendencia de una forma más limpia.
    Al ver a toda galicia observamos que Lugo (la ciudad más fría) se mantiene casi a todo lo largo del año en lo más bajo, cruzandose a veces con Santiago de Compostela. Esto es interesante porque la otra ciudad lejana al mar, Ourense, llega a cruzarse con Santiago y Lugo en temporadas frías de Invierno, pero en Verano es la más calurosa con diferencia. Esto aporta mucho a lo que mencionamos de las temperaturas extremas en ciudades lejanas al mar, porque además Ourense es de las tres la que se encuentra más lejos del mar.
    Por otra parte tenemos las ciudades de Mar y estas se comportan como se espera, todas se mantienen hacia el centro de todas las tendencias, la que se presenta como "más fría" es Coruña y esto tiene sentido porque se encuentra más al norte en comparación al resto.
    
    Luego tenemos la segunda gráfica de Boxplots, aquí se respeta la ligera tendencia en base a las estaciones del año y además de eso que las que tienen la caja más amplia (mayor variación de temperatura) son como ya se ha mencionado antes, las ciudades lejos del mar. 
    """)