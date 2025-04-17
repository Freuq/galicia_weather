import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import folium

# PIE DE LLUVIA
def lluvia_pie(df_conteo, localizacion):
    fig_pie = px.pie(df_conteo, title=f"         Porcentaje de días con y sin lluvia en {localizacion}", names="Tipo de día", values="Cantidad")
    fig_pie.update_traces(
        textinfo="percent+label+value", 
        marker=dict(colors=['#4FC3F7', '#FFEB3B']))
    
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
        margin=dict(l=20, r=20, t=40, b=40))
    
    return fig_pie

# LINEA DE LLUVIA DIARIA
def plot_lluvia_bar(df, localizacion):

    if 'ciudad' in df.columns:
        fig = px.bar(df, x="fecha", y="precipitacion", color="ciudad",
                      title=f"         Precipitación diaria en {localizacion}")
    else:
        fig = px.bar(df, x="fecha", y="precipitacion",
                      title=f"         Precipitación diaria en {localizacion}")

    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='white'),
        title_font=dict(color='white'),
        legend=dict(font=dict(color='white')),
        xaxis=dict(title='Fecha', color='white'),
        yaxis=dict(title='Precipitación (L/m2)', color='white', gridcolor='rgba(255, 255, 255, 0.4)'),
        autosize=True,
        margin=dict(l=20, r=20, t=40, b=40)
    )
    
    return fig

# BARPLOT TEMPERATURA: VARIABLE CATEGÓRICA
def fig_bar_temp_cat(df): 
    fig = px.bar(
        df,
        x='categoria',
        y='count',
        labels={'categoria': 'Categoría de Temperatura', 'count': 'Frecuencia'},
        color='categoria',
        title='         Distribución de días a partir de clasificación de Temperatura'
    )

    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Fondo de la gráfica transparente
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Fondo del paper transparente
        font=dict(color='white'),
        title_font=dict(color='white'),
        legend=dict(font=dict(color='white')),
        xaxis=dict( color='white'),
        yaxis=dict(
            color='white', 
            gridcolor='rgba(255, 255, 255, 0.4)'),
        autosize=True,
        margin=dict(l=20, r=20, t=40, b=40)
    )
    return fig

# LINEA DE TEMPERATURA DIARIA
def plot_temp_line(df, localizacion):

    if 'ciudad' in df.columns:
        fig = px.line(df, x="fecha", y="temperatura", color="ciudad",
                      title=f"         Temperatura diaria en {localizacion}")
    else:
        fig = px.line(df, x="fecha", y="temperatura",
                      title=f"         Temperatura diaria en {localizacion}")

    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='white'),
        title_font=dict(color='white'),
        legend=dict(font=dict(color='white')),
        xaxis=dict(title='Fecha', color='white'),
        yaxis=dict(title='Temperatura (°C)', color='white', gridcolor='rgba(255, 255, 255, 0.4)'),
        autosize=True,
        margin=dict(l=20, r=20, t=40, b=40)
    )
    
    return fig

# BOXPLOT TEMPERATURA POR MES 
def plot_temp_boxplot(df, localizacion):
    if 'ciudad' in df.columns:
        fig = px.box(df, x='mes_nombre', y='temperatura', color='ciudad',
                     title=f'         Distribución mensual de temperatura en {localizacion}')
    else:
        fig = px.box(df, x='mes_nombre', y='temperatura',
                     title=f'         Distribución mensual de temperatura en {localizacion}')
    
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='white'),
        title_font=dict(color='white'),
        legend=dict(font=dict(color='white')),
        xaxis=dict(title='Fecha', color='white'),
        yaxis=dict(title='Temperatura (°C)', color='white', gridcolor='rgba(255, 255, 255, 0.4)'),
        autosize=True,
        margin=dict(l=20, r=20, t=40, b=40)
    )
    
    return fig

# MEDIA MENSUAL POR CIUDAD (LINEA)
def plot_temp_monthly_avg(df, localizacion):
    # Agrupamos por mes (y ciudad si hay varias)
    if 'ciudad' in df.columns:
        df_grouped = df.groupby(['mes_nombre', 'ciudad'])['temperatura'].mean().reset_index()
        fig = px.line(df_grouped, x='mes_nombre', y='temperatura', color='ciudad',
                      markers=True,
                      title=f'         Temperatura media mensual en {localizacion}')
    else:
        df_grouped = df.groupby('mes_nombre')['temperatura'].mean().reset_index()
        fig = px.line(df_grouped, x='mes_nombre', y='temperatura',
                      markers=True,
                      title=f'         Temperatura media mensual en {localizacion}')
    
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='white'),
        title_font=dict(color='white'),
        legend=dict(font=dict(color='white')),
        xaxis=dict(title='Mes', color='white'),
        yaxis=dict(title='Temperatura media (°C)', color='white', gridcolor='rgba(255, 255, 255, 0.4)'),
        autosize=True,
        margin=dict(l=20, r=20, t=40, b=40)
    )
    
    return fig

# LINEA DE TEMPERATURA DIARIA
def plot_humidity_line(df_filtrado, localizacion):
    if 'ciudad' in df_filtrado.columns:
        fig = px.line(df_filtrado, x="fecha", y="humedad", color='ciudad',
                      title=f"         Humedad media diaria en {localizacion}")
    else:
        fig = px.line(df_filtrado, x="fecha", y="humedad",
                      title=f"         Humedad media diaria en {localizacion}")
    
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)', 
        paper_bgcolor='rgba(0, 0, 0, 0)',  
        font=dict(color='white'),
        title_font=dict(color='white'),
        legend=dict(font=dict(color='white')),
        xaxis=dict(title='Fecha', color='white'),
        yaxis=dict(title='Humedad (%)',
                   color='white', 
                   gridcolor='rgba(255, 255, 255, 0.4)'),
        autosize=True,
        margin=dict(l=20, r=20, t=40, b=40)
    )
    
    return fig

# BARPLOT: HUMEDAD EN CATEGORÍAS
def fig_bar_humedad(df, colores):
    fig_bar_hum = px.bar(
        df,
        x='categoria',
        y='count',
        color='categoria',
        color_discrete_map=colores,
        title="Distribución de Humedad por Categoría",
        labels={'categoria': 'Categoría de Humedad', 'humedad': 'Humedad (%)'}
    )

    fig_bar_hum.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='white'),
        title_font=dict(color='white'),
        legend=dict(font=dict(color='white')),
        xaxis=dict(color='white'),
        yaxis=dict(color='white', gridcolor='rgba(255,255,255,0.4)'),
        autosize=True,
        margin=dict(l=20, r=20, t=40, b=40)
    )
    return fig_bar_hum

# DISTRIBUCIÓN DE HUMEDAD (KDE)
def plot_humidity_kde_line(df_filtrado, localizacion):
    fig = go.Figure()

    if 'ciudad' in df_filtrado.columns:
        for ciudad in df_filtrado['ciudad'].unique():
            datos = df_filtrado[df_filtrado['ciudad'] == ciudad]['humedad']
            sns_kde = sns.kdeplot(datos, bw_adjust=1, fill=False)
            x, y = sns_kde.get_lines()[0].get_data()
            sns_kde.figure.clf()  # limpia la figura de seaborn

            fig.add_trace(go.Scatter(
                x=x, y=y,
                mode='lines',
                name=ciudad
            ))
    else:
        sns_kde = sns.kdeplot(df_filtrado['humedad'], bw_adjust=1, fill=False)
        x, y = sns_kde.get_lines()[0].get_data()
        sns_kde.figure.clf()

        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode='lines',
            name=localizacion
        ))

    fig.update_layout(
        title=f'         Distribución suavizada de humedad en {localizacion}',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        title_font=dict(color='white'),
        legend=dict(font=dict(color='white')),
        xaxis=dict(title='Humedad (%)', color='white'),
        yaxis=dict(title='Densidad', color='white', gridcolor='rgba(255,255,255,0.4)'),
        autosize=True,
        margin=dict(l=20, r=20, t=40, b=40)
    )

    return fig

# MAPA DE CALOR (HEATMAP)
def plot_humidity_heatmap(df_filtrado, localizacion):
    df_heatmap = df_filtrado.copy()
    df_heatmap['mes'] = df_heatmap['fecha'].dt.month
    df_heatmap['dia'] = df_heatmap['fecha'].dt.day
    df_heatmap['año'] = df_heatmap['fecha'].dt.year

    # Para simplificar, combinamos año y mes para formar una fila única
    df_heatmap['año_mes'] = df_heatmap['fecha'].dt.to_period('M').astype(str)

    if 'ciudad' in df_heatmap.columns and df_heatmap['ciudad'].nunique() > 1:
        df_heatmap = df_heatmap.groupby(['año_mes', 'ciudad'])['humedad'].mean().reset_index()
        heatmap_data = df_heatmap.pivot(index='ciudad', columns='año_mes', values='humedad')
        title = f"         Mapa de calor de humedad media mensual por ciudad"
    else:
        df_heatmap = df_heatmap.groupby(['año_mes'])['humedad'].mean().reset_index()
        heatmap_data = df_heatmap.pivot_table(index='año_mes', values='humedad')
        title = f"         Mapa de calor de humedad media mensual en {localizacion}"

    fig = px.imshow(
        heatmap_data,
        color_continuous_scale='Blues',
        aspect="auto"
    )

    fig.update_layout(
        title=title,
        xaxis_title="Mes",
        yaxis_title="Ciudad" if 'ciudad' in df_filtrado.columns and df_filtrado['ciudad'].nunique() > 1 else "Fecha",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        #tickfont=dict(color='white'),
        xaxis=dict(color='white'),
        yaxis=dict(color='white'),
        coloraxis_colorbar=dict(title='Humedad (%)', tickfont=dict(color='white')), #titlefont=dict(color='white')),
        autosize=True,
        margin=dict(l=20, r=20, t=40, b=40)
    )

    return fig

#### COMPARATIVAS

# SCATTER PLOT ENTRE TEMP Y HUMEDAD
def plot_temp_vs_humidity(df_filtrado, localizacion):
    if 'ciudad' in df_filtrado.columns and df_filtrado['ciudad'].nunique() > 1:
        fig = px.scatter(df_filtrado, x='temperatura', y='humedad', color='ciudad',
                         title=f'         Relación entre temperatura y humedad en distintas ciudades')
    else:
        fig = px.scatter(df_filtrado, x='temperatura', y='humedad',
                         title=f'         Relación entre temperatura y humedad en {localizacion}')

    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='white'),
        title_font=dict(color='white'),
        legend=dict(font=dict(color='white')),
        xaxis=dict(title='Temperatura (°C)', color='white'),
        yaxis=dict(title='Humedad (%)', color='white'),
        autosize=True,
        margin=dict(l=20, r=20, t=40, b=40)
    )

    return fig

# LINEA CON DOBLE EJE Y: Útil para ver cómo cambian juntas en el tiempo
def plot_temp_humidity_dual_axis(df_filtrado, localizacion):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_filtrado['fecha'], 
        y=df_filtrado['temperatura'], 
        name='Temperatura (°C)', 
        yaxis='y1',
        mode='lines',
        line=dict(color='tomato')
    ))

    fig.add_trace(go.Scatter(
        x=df_filtrado['fecha'], 
        y=df_filtrado['humedad'], 
        name='Humedad (%)', 
        yaxis='y2',
        mode='lines',
        line=dict(color='royalblue')
    ))

    fig.update_layout(
        title=f'         Comparación diaria de temperatura y humedad en {localizacion}',
        xaxis=dict(title='Fecha', color='white'),
        yaxis=dict(
            title='Temperatura (°C)',
            #titlefont=dict(color='tomato'),
            tickfont=dict(color='tomato'),
        ),
        yaxis2=dict(
            title='Humedad (%)',
            #titlefont=dict(color='royalblue'),
            tickfont=dict(color='royalblue'),
            overlaying='y',
            side='right',
        ),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='white'),
        #title_font=dict(color='white'),
        legend=dict(font=dict(color='white')),
        margin=dict(l=20, r=20, t=40, b=40)
    )

    return fig