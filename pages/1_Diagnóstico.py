"""
Página 1: Diagnóstico - Situação Atual das Exportações
"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Adicionar path para imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_processed_data, get_top_countries, calculate_market_concentration
from utils.visualizations import (
    create_line_chart_evolution,
    create_treemap_countries,
    create_horizontal_bar_top_countries,
    create_pie_chart_concentration,
    create_bar_chart_value
)

# Configuração da página
st.set_page_config(
    page_title="Diagnóstico - Wine Export Analysis",
    page_icon="📊",
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
    .alert-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #8B0000;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="big-title">📊 Diagnóstico: Brasil no Mercado Internacional</p>', unsafe_allow_html=True)
st.markdown("### *Onde estamos e o que os números revelam*")
st.markdown("---")

# Carregar dados
df_export, df_import, df_comparacao = load_processed_data()

# Storytelling: Introdução
st.markdown("""
## 🎬 O Cenário Atual

O Brasil possui uma indústria vitivinícola estabelecida, com mais de **200 milhões de litros** 
comercializados anualmente no mercado interno. Mas quando olhamos para o mercado internacional, 
os números contam uma história diferente...
""")

st.markdown("---")

# Seção 1: Volume ao Longo do Tempo
st.markdown('<p class="section-title">📈 Evolução Temporal das Exportações</p>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    # Gráfico de evolução
    fig_evolution = create_line_chart_evolution(
        df_comparacao,
        title="Evolução: Exportação vs Importação (2009-2023)"
    )
    st.plotly_chart(fig_evolution, use_container_width=True)

with col2:
    st.markdown("""
    ### 🔍 O que vemos?
    
    **Exportação (vermelho):**
    - Pico em 2015: ~10M litros
    - Declínio após 2015
    - 2023: apenas ~5.5M litros
    - **Redução de 45% em 8 anos**
    
    **Importação (verde):**
    - Volumes 20-30x maiores
    - Relativamente estável
    - ~140M litros/ano recentemente
    
    **Conclusão:** Brasil é muito mais **importador** do que exportador.
    """)

# Insight Box
st.markdown("""
<div class="alert-box">
<strong>⚠️ Alerta Estratégico:</strong> As exportações brasileiras estão em <strong>tendência de queda</strong>. 
Enquanto isso, mantemos importações altas e estáveis. Precisamos reverter essa tendência.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Seção 2: Valores em USD
st.markdown('<p class="section-title">💰 Comparação de Valores (USD)</p>', unsafe_allow_html=True)

# Gráfico de valores
fig_values = create_bar_chart_value(
    df_comparacao,
    title="Exportação vs Importação - Valores em USD"
)
st.plotly_chart(fig_values, use_container_width=True)

# Métricas de valor
col1, col2, col3, col4 = st.columns(4)

total_exp_valor = df_export['valor_usd'].sum()
total_imp_valor = df_import['valor_usd'].sum()
balanca = total_exp_valor - total_imp_valor

with col1:
    st.metric("💵 Total Exportado", f"US$ {total_exp_valor/1_000_000:.0f}M")

with col2:
    st.metric("💵 Total Importado", f"US$ {total_imp_valor/1_000_000:.0f}M")

with col3:
    st.metric("📉 Déficit Comercial", f"US$ {abs(balanca)/1_000_000:.0f}M", delta_color="inverse")

with col4:
    ratio = total_imp_valor / total_exp_valor
    st.metric("📊 Razão Import/Export", f"{ratio:.1f}x")

st.markdown("""
<div class="alert-box">
<strong>💸 Balança Comercial Negativa:</strong> O Brasil gasta <strong>quase 40x mais</strong> 
importando vinhos do que ganha exportando. Déficit acumulado (2009-2023): <strong>US$ 6+ bilhões</strong>.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Seção 3: Concentração de Mercado
st.markdown('<p class="section-title">🌍 Para Onde Exportamos?</p>', unsafe_allow_html=True)

# Calcular concentração
concentration = calculate_market_concentration(df_export)

# Mostrar métricas de concentração
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🎯 Índice HHI",
        f"{concentration['hhi']:.0f}",
        help="Herfindahl-Hirschman Index: >2500 = alta concentração"
    )

with col2:
    st.metric("🥇 Top 5 Países", f"{concentration['top5_pct']:.1f}%")

with col3:
    st.metric("🏆 Top 10 Países", f"{concentration['top10_pct']:.1f}%")

st.markdown(f"""
<div class="alert-box">
<strong>⚠️ Concentração Extrema:</strong> {concentration['interpretation']} (HHI = {concentration['hhi']:.0f}). 
Os 5 principais destinos respondem por <strong>{concentration['top5_pct']:.1f}%</strong> das exportações.
</div>
""", unsafe_allow_html=True)

# Treemap de países
fig_treemap = create_treemap_countries(
    df_export,
    top_n=15,
    title="Distribuição de Exportações por País (Top 15)"
)
st.plotly_chart(fig_treemap, use_container_width=True)

st.markdown("---")

# Seção 4: Top Países Detalhado
st.markdown('<p class="section-title">🏆 Top 15 Destinos de Exportação</p>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])

with col1:
    # Gráfico de barras horizontais
    fig_top = create_horizontal_bar_top_countries(
        df_export,
        top_n=15,
        title="Volume e Valor por País"
    )
    st.plotly_chart(fig_top, use_container_width=True)

with col2:
    st.markdown("""
    ### 🎯 Destaques
    
    **1️⃣ Paraguai**
    - Domina as exportações
    - ~70% do valor total
    - Mercado de volume/baixo preço
    
    **2️⃣ Haiti**
    - Segundo maior destino
    - ~8% do mercado
    - Crescimento recente
    
    **3️⃣ Uruguai**
    - Terceiro maior
    - ~5% do mercado
    - Mercado Mercosul
    
    **4️⃣ Estados Unidos**
    - Potencial não explorado
    - Apenas ~3% atualmente
    - Mercado premium possível
    
    **5️⃣ China**
    - Mercado emergente
    - ~2% das exportações
    - Alto potencial futuro
    """)

# Tabela detalhada dos top países
st.markdown("### 📋 Tabela Detalhada - Top 15 Países")

top_15 = get_top_countries(df_export, n=15, metric='valor_usd')

# Calcular participação
total_valor = df_export['valor_usd'].sum()
top_15['participacao_pct'] = (top_15['valor_usd'] / total_valor * 100).round(2)

# Formatar valores
top_15_display = top_15.copy()
top_15_display['quantidade_litros'] = top_15_display['quantidade_litros'].apply(lambda x: f"{x:,.0f}")
top_15_display['valor_usd'] = top_15_display['valor_usd'].apply(lambda x: f"US$ {x:,.0f}")
top_15_display['preco_medio'] = top_15_display['preco_medio'].apply(lambda x: f"US$ {x:.2f}/L")
top_15_display['participacao_pct'] = top_15_display['participacao_pct'].apply(lambda x: f"{x:.2f}%")

top_15_display.columns = ['País', 'Volume (litros)', 'Valor (USD)', 'Preço Médio', 'Participação (%)']

st.dataframe(
    top_15_display,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# Seção 5: Concentração Visual (Pizza)
st.markdown('<p class="section-title">🥧 Visualização da Concentração</p>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    fig_pie = create_pie_chart_concentration(
        df_export,
        top_n=5,
        title="Concentração de Mercado - Top 5 + Outros"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.markdown("""
    ### ⚠️ Dependência Crítica
    
    A visualização deixa clara a **dependência extrema do mercado paraguaio**.
    
    **Riscos:**
    - Vulnerabilidade a mudanças políticas/econômicas no Paraguai
    - Instabilidade cambial bilateral
    - Falta de diversificação geográfica
    - Perda de poder de negociação
    
    **Necessidade urgente:**
    Estratégia agressiva de **diversificação de mercados**.
    """)

st.markdown("---")

# Conclusão da página
st.markdown('<p class="section-title">🎯 Síntese do Diagnóstico</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="alert-box">
    <h4>🔴 Problemas Críticos</h4>
    <ul>
        <li>Exportações em queda (-45% desde 2015)</li>
        <li>Déficit comercial de US$ 6+ bilhões</li>
        <li>Concentração extrema (70% Paraguai)</li>
        <li>Baixo valor agregado (US$ 1.92/L)</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="insight-box">
    <h4>🟡 Pontos de Atenção</h4>
    <ul>
        <li>Mercado interno forte (200M L/ano)</li>
        <li>Poucos mercados premium explorados</li>
        <li>Potencial em EUA, China, Reino Unido</li>
        <li>Gap de preço: 66% vs importação</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background-color: #d4edda; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #28a745;">
    <h4>🟢 Oportunidades</h4>
    <ul>
        <li>Base produtiva estabelecida</li>
        <li>Know-how em vinicultura</li>
        <li>Potencial de upgrade qualidade</li>
        <li>Mercados emergentes inexplorados</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.info("➡️ **Próximo passo:** Vá para a página **'🔍 Contexto'** para entender as causas dessa situação e comparar com a concorrência internacional.")