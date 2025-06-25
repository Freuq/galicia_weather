# ⛅Morriña en Galicia o Galizia Weather  
Este proyecto es sobre el clima de Galicia y sus seis ciudades, en particular sobre tres variables: La temperatura, las precipitaciones y la humedad relativa. Realizado netamente en Python.  
## Motivo  
Estuve poco más de dos años viviendo en Galicia y siempre me dijeron que en esta zona llovía mucho y que antes inclusive más, que "el frío de galicia es diferente, se te mete a los huesos".  
Esto siempre despertó curiosidad en mi, preguntandome ¿cuántos días llovian al año?, ¿cuánto frío habrá?, ¿será que este "frío en los huesos" es por la humedad"? y muchas otras preguntas que no sabía cómo contestar.  
Por lo que decidí hacer este proyecto. Que tiene como finalidad responder varias de estas preguntas que despertaron mi curiosidad.  
## Proyecto  
Este proyecto contiene los datos de las ciudades más grandes de Galicia (Coruña, Lugo, Ourense, Vigo, Pontevedra y Santiago de Compostela) donde haré un análisis de datos desde 1 de Enero del 2023 hasta el 1 de Marzo del 2025. Para responder algunas de estas preguntas ya mencionadas, realizar otro tipo de estudias, comparaciones y predicciones.  
### Datos  
Todos los datos fueron obtenidos de [MeteoGalicia](https://www.meteogalicia.gal) y de su API [MeteoSIX](https://www.meteogalicia.gal/web/modelos-numericos/meteosix).  
Comprenden el periodo desde 1ro de Enero del 2023 hasta el 31 de Marzo del 2025. Con tres variables de interés: Precipitación, Temperatura y Humedad.
### Herramientas
La gran parte del proyecto está escrita en Python, tiene una sección en CSS para poder editar todo el segmento de Streamlit.  
Las librerías utilizadas son: Pandas, OS, Streamlit, Plotly, Seaborn, Folium, entre otras.
## Preparación
Los datos obtenidos por MeteoGalicia vienen dados en CSV, ellos tienen una interfaz gráfica para obtener estos datos desde su página, es sencilla y se pueden obtener datos hasta más de 10 años, pero sólo de 1 punto a la vez. Por otra parte los de Forecast se obtienen de la API MeteoSIX en JSON.    
### Total de datos
Por lo que contamos con 6 tablas (una para cada ciudad) de un total de 4 columnas (fecha, humedad, precipitación y temperatura) y 821 filas (una fila equivaldría a un día). Siendo un total de casi 5000 datos.  
Mientras que para el forecast sería 6 tablas temporales (una por cada ciudad), y 5 columnas (aquí se añade sky_state o estado de cielo a las columnas). Siendo un total de 144 datos, si tomamos en cuenta todas las tablas.
## Proceso
El proceso fue sencillo, ya que los datos son dados en CSV y con él se realizó un pequeño script (cleanWeatherData.py) para pivotar la tabla de forma que se pudiese concatenar dichas tablas en una sola y generar una columna "ciudad" que contenga la ciudad de la tabla. Para el dataframe de predicción también se generó un script (cleanForecastInfo.py) pero este convirtiendo el JSON en un DataFrame, el cual también hace petición de estado del cielo y se encuentra en horas, por lo que habrá 24 datos para ver la evolución horaria del día a predecir. Ambas dos se encuentran en la carpeta data/cleaning  
