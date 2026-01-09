"""
Wine Export Analysis - Tech Challenge Fase 1
Página inicial do aplicativo Streamlit

Autor: Leandro Tanno (POSTECH Data Analytics)
"""
import streamlit as st
import pandas as pd
from pathlib import Path

# Configuração da página
st.set_page_config(
    page_title="Vinhos do Brasil: Rumo ao Mercado Premium",
    page_icon="🍷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #8B0000;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4A4A4A;
        text-align: center;
        margin-top: 0;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f0f0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #8B0000;
    }
    .highlight-box {
        background-color: #fff9e6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #DAA520;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">🍷 Vinhos do Brasil: Rumo ao Mercado Premium</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Análise Estratégica das Exportações Brasileiras de Vinho (2009-2023)</p>', unsafe_allow_html=True)

# Linha separadora
st.markdown("---")

# Introdução
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ## 📋 Sobre o Projeto
    
    Este projeto analisa **15 anos de dados** (2009-2023) das exportações brasileiras de vinho, 
    com o objetivo de identificar oportunidades estratégicas para transformar o Brasil em um 
    **player relevante no mercado internacional de vinhos premium**.
    
    ### 🎯 Pergunta Norteadora
    
    > *"Como o Brasil pode evoluir de um modelo de volume/baixo valor para um posicionamento 
    > competitivo no mercado internacional de vinhos premium?"*
    
    ### 📊 Dados Analisados
    
    - **Exportações**: 137 países destino | Volume e valor (USD)
    - **Importações**: 68 países origem | Análise comparativa
    - **Produção**: Categorias e volumes produzidos
    - **Processamento**: Cultivares processadas
    - **Comercialização**: Mercado interno brasileiro
    
    **Fonte**: EMBRAPA Vitibrasil
    """)

with col2:
    st.markdown("""
    ### 🚀 Navegação
    
    Use o menu lateral para explorar:
    
    **📊 Diagnóstico**
    - Situação atual das exportações
    - Principais destinos
    - Análise de volume e valor
    
    **🔍 Contexto**
    - Comparação Export vs Import
    - Análise de preços
    - Posicionamento competitivo
    
    **🎯 Estratégias**
    - Oportunidades identificadas
    - Recomendações acionáveis
    - Projeções futuras
    """)

st.markdown("---")

# KPIs Principais
st.markdown("## 📈 Métricas Gerais (2009-2023)")

try:
    # Carregar dados processados
    data_path = Path('data/processed')
    df_export = pd.read_csv(data_path / 'export_processed.csv')
    df_import = pd.read_csv(data_path / 'import_processed.csv')
    df_comparacao = pd.read_csv(data_path / 'comparacao_exp_imp.csv')
    
    # Calcular métricas
    total_export_litros = df_export['quantidade_litros'].sum()
    total_export_usd = df_export['valor_usd'].sum()
    preco_medio_exp = total_export_usd / total_export_litros
    
    total_import_litros = df_import['quantidade_litros'].sum()
    total_import_usd = df_import['valor_usd'].sum()
    preco_medio_imp = total_import_usd / total_import_litros
    
    num_paises_destino = df_export['pais_destino'].nunique()
    
    # Balança comercial
    balanca_litros = total_export_litros - total_import_litros
    balanca_usd = total_export_usd - total_import_usd
    
    # Display métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🌍 Países Destino",
            value=f"{num_paises_destino}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="📦 Total Exportado",
            value=f"{total_export_litros/1_000_000:.1f}M L",
            delta=None
        )
    
    with col3:
        st.metric(
            label="💰 Valor Total Export",
            value=f"US$ {total_export_usd/1_000_000:.0f}M",
            delta=None
        )
    
    with col4:
        st.metric(
            label="💵 Preço Médio Export",
            value=f"US$ {preco_medio_exp:.2f}/L",
            delta=None
        )
    
    st.markdown("---")
    
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric(
            label="📥 Total Importado",
            value=f"{total_import_litros/1_000_000:.1f}M L",
            delta=None
        )
    
    with col6:
        st.metric(
            label="💰 Valor Total Import",
            value=f"US$ {total_import_usd/1_000_000:.0f}M",
            delta=None
        )
    
    with col7:
        st.metric(
            label="💵 Preço Médio Import",
            value=f"US$ {preco_medio_imp:.2f}/L",
            delta=None
        )
    
    with col8:
        diferenca_preco = ((preco_medio_imp / preco_medio_exp) - 1) * 100
        st.metric(
            label="📊 Diferença de Preço",
            value=f"+{diferenca_preco:.1f}%",
            delta="Import > Export",
            delta_color="inverse"
        )

except FileNotFoundError:
    st.error("❌ Erro ao carregar dados. Execute `python utils/data_processing.py` primeiro.")
    st.stop()

st.markdown("---")

# Insights Principais
st.markdown("## 💡 Principais Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="highlight-box">
    <h3>🔴 Desafios Identificados</h3>
    <ul>
        <li><strong>Concentração extrema:</strong> ~70% das exportações vão para o Paraguai</li>
        <li><strong>Baixo valor agregado:</strong> Preço médio de US$ 1.92/L (vinho de mesa)</li>
        <li><strong>Balança negativa:</strong> Importamos 25x mais do que exportamos em volume</li>
        <li><strong>Gap de preço:</strong> Importamos vinhos 66% mais caros do que exportamos</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="highlight-box">
    <h3>🟢 Oportunidades Identificadas</h3>
    <ul>
        <li><strong>Mercados crescentes:</strong> China, EUA e Reino Unido com potencial</li>
        <li><strong>Produção robusta:</strong> 200M+ litros comercializados internamente</li>
        <li><strong>Diversificação:</strong> Reduzir dependência do mercado paraguaio</li>
        <li><strong>Premium:</strong> Desenvolver vinhos finos e espumantes de qualidade</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Metodologia
with st.expander("📚 Metodologia e Fontes de Dados"):
    st.markdown("""
    ### Metodologia
    
    1. **Coleta de Dados**: Extração de dados da plataforma Embrapa Vitibrasil
    2. **Processamento**: Transformação de formato wide para long, limpeza e agregações
    3. **Análise Exploratória**: Identificação de padrões, tendências e outliers
    4. **Visualização**: Criação de dashboards interativos com Plotly
    5. **Insights**: Geração de recomendações estratégicas baseadas em dados
    
    ### Conversão de Unidades
    
    Conforme especificado no enunciado: **1 kg = 1 litro**
    
    ### Período de Análise
    
    **2009-2023** (últimos 15 anos conforme solicitado)
    
    ### Fontes
    
    - **EMBRAPA Vitibrasil**: http://vitibrasil.cnpuv.embrapa.br
    - Datasets: Exportação, Importação, Produção, Processamento, Comercialização
    
    ### Tecnologias Utilizadas
    
    - **Python 3.12**: Linguagem principal
    - **Pandas**: Manipulação de dados
    - **Plotly**: Visualizações interativas
    - **Streamlit**: Interface web
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><strong>Tech Challenge Fase 1 - POSTECH Data Analytics</strong></p>
    <p>Desenvolvido por Tanno | 2025</p>
</div>
""", unsafe_allow_html=True)