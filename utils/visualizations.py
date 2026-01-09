"""
Funções de visualização com Plotly para o projeto Wine Export Analysis
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


# Paleta de cores do projeto
COLORS = {
    'primary': '#8B0000',      # Vinho tinto
    'secondary': '#DAA520',    # Dourado
    'accent': '#2E8B57',       # Verde uvas
    'neutral': '#4A4A4A',      # Grafite
    'background': '#F5F5F5',   # Cinza claro
    'warning': '#FF6B6B',      # Vermelho suave
    'success': '#4ECDC4',      # Turquesa
    'purple': '#9B59B6',       # Roxo
    'orange': '#E67E22'        # Laranja
}


def create_line_chart_evolution(df_comparacao, title="Evolução Exportação vs Importação"):
    """
    Gráfico de linhas comparando evolução temporal de exportação e importação.
    
    Args:
        df_comparacao: DataFrame com comparação anual
        title: Título do gráfico
        
    Returns:
        plotly.graph_objects.Figure
    """
    fig = go.Figure()
    
    # Linha de Exportação - Volume
    fig.add_trace(go.Scatter(
        x=df_comparacao['ano'],
        y=df_comparacao['exp_litros'] / 1_000_000,  # Converter para milhões
        name='Exportação (volume)',
        line=dict(color=COLORS['primary'], width=3),
        mode='lines+markers',
        hovertemplate='<b>%{x}</b><br>Exportação: %{y:.1f}M litros<extra></extra>'
    ))
    
    # Linha de Importação - Volume
    fig.add_trace(go.Scatter(
        x=df_comparacao['ano'],
        y=df_comparacao['imp_litros'] / 1_000_000,
        name='Importação (volume)',
        line=dict(color=COLORS['accent'], width=3),
        mode='lines+markers',
        hovertemplate='<b>%{x}</b><br>Importação: %{y:.1f}M litros<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color=COLORS['neutral'])),
        xaxis_title='Ano',
        yaxis_title='Volume (Milhões de Litros)',
        hovermode='x unified',
        template='plotly_white',
        height=500,
        font=dict(family='Arial', size=12),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig


def create_bar_chart_value(df_comparacao, title="Comparação de Valores (USD)"):
    """
    Gráfico de barras comparando valores em USD.
    
    Args:
        df_comparacao: DataFrame com comparação anual
        title: Título do gráfico
        
    Returns:
        plotly.graph_objects.Figure
    """
    fig = go.Figure()
    
    # Barras de Exportação
    fig.add_trace(go.Bar(
        x=df_comparacao['ano'],
        y=df_comparacao['exp_usd'] / 1_000_000,  # Milhões
        name='Exportação',
        marker_color=COLORS['primary'],
        hovertemplate='<b>%{x}</b><br>Exportação: US$ %{y:.1f}M<extra></extra>'
    ))
    
    # Barras de Importação
    fig.add_trace(go.Bar(
        x=df_comparacao['ano'],
        y=df_comparacao['imp_usd'] / 1_000_000,
        name='Importação',
        marker_color=COLORS['accent'],
        hovertemplate='<b>%{x}</b><br>Importação: US$ %{y:.1f}M<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color=COLORS['neutral'])),
        xaxis_title='Ano',
        yaxis_title='Valor (Milhões USD)',
        barmode='group',
        template='plotly_white',
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig


def create_treemap_countries(df_export, top_n=15, title="Distribuição por País Destino"):
    """
    Treemap mostrando distribuição de exportações por país.
    
    Args:
        df_export: DataFrame de exportações
        top_n: Número de países a mostrar
        title: Título do gráfico
        
    Returns:
        plotly.graph_objects.Figure
    """
    # Agregar por país
    pais_agg = df_export.groupby('pais_destino').agg({
        'valor_usd': 'sum',
        'quantidade_litros': 'sum'
    }).reset_index()
    
    pais_agg['preco_medio'] = pais_agg['valor_usd'] / pais_agg['quantidade_litros']
    pais_agg = pais_agg.nlargest(top_n, 'valor_usd')
    
    # Calcular participação percentual
    total_valor = pais_agg['valor_usd'].sum()
    pais_agg['participacao'] = (pais_agg['valor_usd'] / total_valor * 100).round(1)
    
    # Labels customizados
    pais_agg['label'] = pais_agg.apply(
        lambda x: f"{x['pais_destino']}<br>{x['participacao']:.1f}%<br>US$ {x['preco_medio']:.2f}/L",
        axis=1
    )
    
    fig = go.Figure(go.Treemap(
        labels=pais_agg['label'],
        parents=[''] * len(pais_agg),
        values=pais_agg['valor_usd'],
        marker=dict(
            colorscale='RdYlGn',
            cmid=pais_agg['preco_medio'].median(),
            colorbar=dict(title="Preço Médio<br>(USD/L)")
        ),
        text=pais_agg['pais_destino'],
        hovertemplate='<b>%{text}</b><br>Valor: US$ %{value:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color=COLORS['neutral'])),
        height=600,
        template='plotly_white'
    )
    
    return fig


def create_horizontal_bar_top_countries(df_export, top_n=15, title="Top 15 Países Destino"):
    """
    Gráfico de barras horizontais com top países.
    
    Args:
        df_export: DataFrame de exportações
        top_n: Número de países
        title: Título
        
    Returns:
        plotly.graph_objects.Figure
    """
    # Agregar e ordenar
    top_paises = df_export.groupby('pais_destino').agg({
        'quantidade_litros': 'sum',
        'valor_usd': 'sum'
    }).reset_index()
    
    top_paises['preco_medio'] = top_paises['valor_usd'] / top_paises['quantidade_litros']
    top_paises = top_paises.nlargest(top_n, 'valor_usd').sort_values('valor_usd')
    
    fig = go.Figure()
    
    # Barras de volume
    fig.add_trace(go.Bar(
        y=top_paises['pais_destino'],
        x=top_paises['quantidade_litros'] / 1_000_000,
        name='Volume (M litros)',
        orientation='h',
        marker_color=COLORS['secondary'],
        hovertemplate='<b>%{y}</b><br>Volume: %{x:.2f}M litros<extra></extra>'
    ))
    
    # Barras de valor
    fig.add_trace(go.Bar(
        y=top_paises['pais_destino'],
        x=top_paises['valor_usd'] / 1_000_000,
        name='Valor (M USD)',
        orientation='h',
        marker_color=COLORS['primary'],
        hovertemplate='<b>%{y}</b><br>Valor: US$ %{x:.2f}M<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color=COLORS['neutral'])),
        xaxis_title='Milhões',
        barmode='group',
        template='plotly_white',
        height=600,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig


def create_scatter_price_volume(df_export, title="Preço Médio vs Volume por País"):
    """
    Scatter plot mostrando relação entre preço e volume.
    
    Args:
        df_export: DataFrame de exportações
        title: Título
        
    Returns:
        plotly.graph_objects.Figure
    """
    # Agregar por país
    pais_agg = df_export.groupby('pais_destino').agg({
        'valor_usd': 'sum',
        'quantidade_litros': 'sum'
    }).reset_index()
    
    pais_agg['preco_medio'] = pais_agg['valor_usd'] / pais_agg['quantidade_litros']
    
    # Remover outliers extremos para melhor visualização
    pais_agg = pais_agg[pais_agg['preco_medio'] < 10]
    
    fig = px.scatter(
        pais_agg,
        x='quantidade_litros',
        y='preco_medio',
        size='valor_usd',
        hover_name='pais_destino',
        color='preco_medio',
        color_continuous_scale='RdYlGn',
        labels={
            'quantidade_litros': 'Volume Total (Litros)',
            'preco_medio': 'Preço Médio (USD/L)',
            'valor_usd': 'Valor Total (USD)'
        },
        title=title
    )
    
    fig.update_layout(
        template='plotly_white',
        height=600,
        title=dict(font=dict(size=20, color=COLORS['neutral']))
    )
    
    fig.update_traces(
        hovertemplate='<b>%{hovertext}</b><br>Volume: %{x:,.0f} L<br>Preço: US$ %{y:.2f}/L<extra></extra>'
    )
    
    return fig


def create_line_chart_price_trends(df_comparacao, title="Evolução do Preço Médio"):
    """
    Linha mostrando evolução dos preços médios.
    
    Args:
        df_comparacao: DataFrame com comparação
        title: Título
        
    Returns:
        plotly.graph_objects.Figure
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_comparacao['ano'],
        y=df_comparacao['preco_medio_exp'],
        name='Exportação',
        line=dict(color=COLORS['primary'], width=3),
        mode='lines+markers',
        hovertemplate='<b>%{x}</b><br>Preço Export: US$ %{y:.2f}/L<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=df_comparacao['ano'],
        y=df_comparacao['preco_medio_imp'],
        name='Importação',
        line=dict(color=COLORS['accent'], width=3),
        mode='lines+markers',
        hovertemplate='<b>%{x}</b><br>Preço Import: US$ %{y:.2f}/L<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color=COLORS['neutral'])),
        xaxis_title='Ano',
        yaxis_title='Preço Médio (USD/L)',
        template='plotly_white',
        height=500,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig


def create_gauge_chart(value, title, max_value=100, threshold_green=70, threshold_yellow=40):
    """
    Gráfico de gauge para KPIs.
    
    Args:
        value: Valor atual
        title: Título do gauge
        max_value: Valor máximo
        threshold_green: Limite para zona verde
        threshold_yellow: Limite para zona amarela
        
    Returns:
        plotly.graph_objects.Figure
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        title={'text': title, 'font': {'size': 18}},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': COLORS['primary']},
            'steps': [
                {'range': [0, threshold_yellow], 'color': COLORS['warning']},
                {'range': [threshold_yellow, threshold_green], 'color': COLORS['secondary']},
                {'range': [threshold_green, max_value], 'color': COLORS['success']}
            ],
            'threshold': {
                'line': {'color': COLORS['neutral'], 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        template='plotly_white'
    )
    
    return fig


def create_area_chart_stacked(df_data, title="Distribuição ao Longo do Tempo"):
    """
    Gráfico de área empilhada.
    
    Args:
        df_data: DataFrame com dados temporais
        title: Título
        
    Returns:
        plotly.graph_objects.Figure
    """
    fig = go.Figure()
    
    # Exemplo genérico - adaptar conforme necessidade
    for col in df_data.columns[1:]:  # Pular primeira coluna (anos)
        fig.add_trace(go.Scatter(
            x=df_data.iloc[:, 0],
            y=df_data[col],
            name=col,
            mode='lines',
            stackgroup='one',
            fillcolor='tonexty'
        ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color=COLORS['neutral'])),
        xaxis_title='Ano',
        yaxis_title='Volume',
        template='plotly_white',
        height=500,
        hovermode='x unified'
    )
    
    return fig


def create_pie_chart_concentration(df_export, top_n=5, title="Concentração de Mercado"):
    """
    Gráfico de pizza mostrando concentração nos top N países.
    
    Args:
        df_export: DataFrame de exportações
        top_n: Número de países top
        title: Título
        
    Returns:
        plotly.graph_objects.Figure
    """
    # Agregar
    pais_total = df_export.groupby('pais_destino')['valor_usd'].sum().sort_values(ascending=False)
    
    # Top N e resto
    top = pais_total.head(top_n)
    resto = pais_total.iloc[top_n:].sum()
    
    # Criar DataFrame para o gráfico
    data = pd.DataFrame({
        'pais': list(top.index) + ['Outros'],
        'valor': list(top.values) + [resto]
    })
    
    fig = px.pie(
        data,
        values='valor',
        names='pais',
        title=title,
        color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['accent'], 
                                 COLORS['purple'], COLORS['orange'], COLORS['neutral']]
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Valor: US$ %{value:,.0f}<br>Participação: %{percent}<extra></extra>'
    )
    
    fig.update_layout(
        template='plotly_white',
        height=500,
        title=dict(font=dict(size=20, color=COLORS['neutral']))
    )
    
    return fig