"""
Página 2: Contexto - Análise Aprofundada e Comparativa
"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Adicionar path para imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_processed_data, get_top_countries
from utils.visualizations import (
    create_line_chart_price_trends,
    create_scatter_price_volume,
    create_bar_chart_value,
    COLORS
)
import plotly.graph_objects as go
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Contexto - Wine Export Analysis",
    page_icon="🔍",
    layout="wide"
)

# CSS
st.markdown("""
<style>
    .big-title {
        font-size: 2.5rem;
        color: #8B0000;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .section-title {
        font-size: 1.8rem;
        color: #4A4A4A;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid #8B0000;
        padding-bottom: 0.5rem;
    }
    .insight-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #DAA520;
        margin: 1rem 0;
    }
    .comparison-box {
        background-color: #e7f3ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E8B57;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="big-title">🔍 Contexto: Entendendo o Posicionamento</p>', unsafe_allow_html=True)
st.markdown("### *Por que exportamos pouco e barato? Análise comparativa e estrutural*")
st.markdown("---")

# Carregar dados
df_export, df_import, df_comparacao = load_processed_data()

# Storytelling: Introdução
st.markdown("""
## 🎭 A Equação do Vinho Brasileiro

No diagnóstico, vimos **O QUE** está acontecendo: exportamos pouco, para poucos países, a preços baixos.
Agora vamos entender **POR QUE** isso acontece e como nos comparamos com a concorrência internacional.
""")

st.markdown("---")

# Seção 1: A Grande Questão do Preço
st.markdown('<p class="section-title">💰 A Diferença de Preço: Export vs Import</p>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    # Gráfico de evolução de preços
    fig_prices = create_line_chart_price_trends(
        df_comparacao,
        title="Evolução do Preço Médio: Exportação vs Importação"
    )
    st.plotly_chart(fig_prices, use_container_width=True)

with col2:
    # Calcular estatísticas
    preco_exp_medio = df_comparacao['preco_medio_exp'].mean()
    preco_imp_medio = df_comparacao['preco_medio_imp'].mean()
    diferenca_pct = ((preco_imp_medio / preco_exp_medio) - 1) * 100
    
    st.markdown(f"""
    ### 📊 Estatísticas
    
    **Preço Médio Export:**
    - US$ {preco_exp_medio:.2f}/L
    - Vinho de mesa barato
    - Mercado de volume
    
    **Preço Médio Import:**
    - US$ {preco_imp_medio:.2f}/L
    - Vinhos finos/premium
    - Mercado de valor
    
    **Gap:**
    - +{diferenca_pct:.1f}% mais caro
    - Diferença de qualidade
    - Posicionamento distinto
    """)

st.markdown(f"""
<div class="insight-box">
<strong>💡 Insight Crítico:</strong> O Brasil <strong>exporta vinho de mesa</strong> (baixo valor) 
mas <strong>importa vinho fino</strong> (alto valor). Estamos competindo no segmento errado do mercado global.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Seção 2: Quem são nossos concorrentes (de onde importamos)
st.markdown('<p class="section-title">🌎 De Onde Importamos? (Nossos Concorrentes)</p>', unsafe_allow_html=True)

# Top países de importação
top_origem = df_import.groupby('pais_origem').agg({
    'quantidade_litros': 'sum',
    'valor_usd': 'sum'
}).reset_index()
top_origem['preco_medio'] = top_origem['valor_usd'] / top_origem['quantidade_litros']
top_origem = top_origem.sort_values('valor_usd', ascending=False).head(10)

# Gráfico de barras dos importadores
fig = go.Figure()

fig.add_trace(go.Bar(
    y=top_origem['pais_origem'][::-1],
    x=top_origem['quantidade_litros'][::-1] / 1_000_000,
    name='Volume (M litros)',
    orientation='h',
    marker_color=COLORS['accent'],
    text=top_origem['quantidade_litros'][::-1] / 1_000_000,
    texttemplate='%{text:.1f}M',
    textposition='outside'
))

fig.update_layout(
    title="Top 10 Países de Importação - Volume",
    xaxis_title="Milhões de Litros",
    template='plotly_white',
    height=500,
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# Tabela comparativa
st.markdown("### 📋 Comparação: Exportação BR vs Principais Importadores")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🇧🇷 O que EXPORTAMOS")
    top_exp = get_top_countries(df_export, n=5, metric='valor_usd')
    top_exp_display = top_exp[['pais_destino', 'preco_medio']].copy()
    top_exp_display['preco_medio'] = top_exp_display['preco_medio'].apply(lambda x: f"US$ {x:.2f}/L")
    top_exp_display.columns = ['País', 'Preço Médio']
    st.dataframe(top_exp_display, hide_index=True, use_container_width=True)

with col2:
    st.markdown("#### 🌍 O que IMPORTAMOS")
    top_imp_display = top_origem.head(5)[['pais_origem', 'preco_medio']].copy()
    top_imp_display['preco_medio'] = top_imp_display['preco_medio'].apply(lambda x: f"US$ {x:.2f}/L")
    top_imp_display.columns = ['País', 'Preço Médio']
    st.dataframe(top_imp_display, hide_index=True, use_container_width=True)

st.markdown("""
<div class="comparison-box">
<strong>🔍 Comparação:</strong><br>
<strong>Exportamos para:</strong> Paraguai, Haiti, Uruguai - Mercados de volume/baixo custo<br>
<strong>Importamos de:</strong> Chile, Argentina, Portugal, Itália, França - Produtores premium reconhecidos mundialmente<br><br>
<strong>Conclusão:</strong> Competimos no segmento de <strong>commodities</strong>, não no de <strong>especialidades</strong>.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Seção 3: Análise de Segmentação por Preço
st.markdown('<p class="section-title">🎯 Segmentação por Preço: Onde Estamos?</p>', unsafe_allow_html=True)

# Calcular segmentação
pais_preco = df_export.groupby('pais_destino').agg({
    'valor_usd': 'sum',
    'quantidade_litros': 'sum'
}).reset_index()
pais_preco['preco_medio'] = pais_preco['valor_usd'] / pais_preco['quantidade_litros']

# Classificar por faixa
def classify_price(price):
    if price < 1.5:
        return 'Baixo (<US$ 1.50/L)'
    elif price < 3.0:
        return 'Médio (US$ 1.50-3.00/L)'
    else:
        return 'Alto (>US$ 3.00/L)'

pais_preco['faixa'] = pais_preco['preco_medio'].apply(classify_price)

# Agregar por faixa
faixa_agg = pais_preco.groupby('faixa').agg({
    'valor_usd': 'sum',
    'quantidade_litros': 'sum',
    'pais_destino': 'count'
}).reset_index()

faixa_agg.columns = ['Faixa de Preço', 'Valor Total (USD)', 'Volume Total (L)', 'Nº Países']

# Calcular percentuais
faixa_agg['% Valor'] = (faixa_agg['Valor Total (USD)'] / faixa_agg['Valor Total (USD)'].sum() * 100).round(1)
faixa_agg['% Volume'] = (faixa_agg['Volume Total (L)'] / faixa_agg['Volume Total (L)'].sum() * 100).round(1)

col1, col2 = st.columns([1, 1])

with col1:
    # Gráfico de pizza - Distribuição de valor por faixa
    fig_pie = go.Figure(data=[go.Pie(
        labels=faixa_agg['Faixa de Preço'],
        values=faixa_agg['Valor Total (USD)'],
        marker=dict(colors=[COLORS['warning'], COLORS['secondary'], COLORS['success']]),
        hole=0.3
    )])
    
    fig_pie.update_layout(
        title="Distribuição de Valor por Faixa de Preço",
        template='plotly_white',
        height=400
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.markdown("### 📊 Análise por Faixa")
    st.dataframe(
        faixa_agg[['Faixa de Preço', '% Valor', '% Volume', 'Nº Países']],
        hide_index=True,
        use_container_width=True
    )

st.markdown("""
<div class="insight-box">
<strong>💡 Revelação:</strong> A maior parte das nossas exportações está concentrada na <strong>faixa de baixo preço</strong> 
(menos de US$ 1.50/L). Pouquíssimo volume vai para o segmento premium (>US$ 3.00/L).
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Seção 4: Scatter Plot - Preço vs Volume
st.markdown('<p class="section-title">📊 Matriz: Preço vs Volume por País</p>', unsafe_allow_html=True)

fig_scatter = create_scatter_price_volume(
    df_export,
    title="Análise de Posicionamento: Preço Médio vs Volume Exportado"
)
st.plotly_chart(fig_scatter, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🔴 Quadrante Atual (maioria)
    
    **Características:**
    - Alto volume, baixo preço
    - Paraguai domina este quadrante
    - Mercado de commodities
    - Baixa margem
    
    **Estratégia atual:**
    Competir por **volume**, não por **valor**.
    """)

with col2:
    st.markdown("""
    ### 🟢 Quadrante Desejado
    
    **Características:**
    - Preço premium (>US$ 3/L)
    - Volume menor, mais seletivo
    - Mercados desenvolvidos
    - Alta margem
    
    **Estratégia necessária:**
    Migrar para **qualidade** e **diferenciação**.
    """)

st.markdown("---")

# Seção 5: Balança Comercial Detalhada
st.markdown('<p class="section-title">⚖️ Balança Comercial: O Déficit Estrutural</p>', unsafe_allow_html=True)

# Gráfico de área - Balança ao longo do tempo
fig_balanca = go.Figure()

fig_balanca.add_trace(go.Scatter(
    x=df_comparacao['ano'],
    y=df_comparacao['exp_usd'] / 1_000_000,
    name='Exportação',
    fill='tozeroy',
    line=dict(color=COLORS['primary']),
    mode='lines'
))

fig_balanca.add_trace(go.Scatter(
    x=df_comparacao['ano'],
    y=df_comparacao['imp_usd'] / 1_000_000,
    name='Importação',
    fill='tozeroy',
    line=dict(color=COLORS['accent']),
    mode='lines'
))

fig_balanca.update_layout(
    title="Balança Comercial: Exportação vs Importação (Milhões USD)",
    xaxis_title="Ano",
    yaxis_title="Valor (Milhões USD)",
    template='plotly_white',
    height=500,
    hovermode='x unified'
)

st.plotly_chart(fig_balanca, use_container_width=True)

# Métricas de balança
total_deficit = df_comparacao['balanca_usd'].sum()
deficit_medio_anual = df_comparacao['balanca_usd'].mean()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "💸 Déficit Acumulado (2009-2023)",
        f"US$ {abs(total_deficit)/1_000_000:.0f}M"
    )

with col2:
    st.metric(
        "📉 Déficit Médio Anual",
        f"US$ {abs(deficit_medio_anual)/1_000_000:.0f}M"
    )

with col3:
    ratio_medio = df_comparacao['imp_usd'].sum() / df_comparacao['exp_usd'].sum()
    st.metric(
        "📊 Razão Import/Export",
        f"{ratio_medio:.1f}x"
    )

st.markdown("""
<div class="insight-box">
<strong>💸 Impacto Econômico:</strong> Nos últimos 15 anos, o Brasil teve um déficit acumulado de 
<strong>mais de US$ 6 bilhões</strong> na balança comercial de vinhos. Isso significa que gastamos 
muito mais importando vinhos premium do que ganhamos exportando vinhos de mesa.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Seção 6: Por que isso acontece?
st.markdown('<p class="section-title">❓ Por Que Estamos Nessa Situação?</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🔴 Fatores Estruturais
    
    **1. Posicionamento Histórico**
    - Tradição em vinhos de mesa
    - Foco no mercado interno
    - Produção de volume vs qualidade
    
    **2. Geografia e Clima**
    - Maioria da produção em regiões úmidas
    - Clima tropical/subtropical
    - Desafios para vinhos finos
    
    **3. Competição Internacional**
    - Chile e Argentina dominam América do Sul
    - Europa tem tradição milenar
    - Austrália/Nova Zelândia em expansão
    
    **4. Mercado Interno Forte**
    - 200M litros comercializados localmente
    - Pouco incentivo para exportar
    - Conforto do mercado doméstico
    """)

with col2:
    st.markdown("""
    ### 🟢 Potencial Não Explorado
    
    **1. Vale dos Vinhedos**
    - Região reconhecida internacionalmente
    - Vinhos finos de qualidade
    - Ainda pouco explorado no exterior
    
    **2. Espumantes**
    - Brasil produz espumantes de qualidade
    - Potencial para mercados premium
    - Exportação ainda tímida
    
    **3. Vinhos Orgânicos**
    - Tendência global crescente
    - Brasil tem know-how
    - Nicho com alto valor agregado
    
    **4. Inovação**
    - Novas técnicas de vinificação
    - Cultivares adaptados ao clima
    - Oportunidade de diferenciação
    """)

st.markdown("---")

# Conclusão da página
st.markdown('<p class="section-title">🎯 Síntese do Contexto</p>', unsafe_allow_html=True)

st.markdown("""
## 📝 O Que Aprendemos?

**1. Posicionamento Inadequado**
- Competimos no segmento de baixo valor (commodities)
- Enquanto importamos do segmento premium (especialidades)
- Gap de preço: +127% entre import e export

**2. Concorrência Desigual**
- Nossos principais "concorrentes" (Chile, Argentina, Portugal) vendem no Brasil a preços 66% maiores
- Exportamos para mercados de menor poder aquisitivo
- Falta presença em mercados premium (Europa, América do Norte)

**3. Déficit Estrutural**
- Balança comercial negativa há 15 anos
- Déficit acumulado: US$ 6+ bilhões
- Importamos 25x mais do que exportamos (em volume)

**4. Oportunidade Clara**
- Brasil tem capacidade produtiva
- Regiões com potencial para vinhos finos (Vale dos Vinhedos)
- Espumantes e orgânicos como nichos promissores
- Mercado interno forte indica know-how

## 🚀 Próximo Passo

Agora que entendemos **ONDE** estamos e **POR QUE** estamos assim, 
precisamos definir **PARA ONDE** ir. Na próxima seção, vamos explorar 
estratégias concretas e acionáveis para transformar esse cenário.
""")

st.info("➡️ **Próximo passo:** Vá para a página **'🎯 Estratégias'** para ver as recomendações baseadas em dados e projeções futuras.")