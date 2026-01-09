"""
Página 3: Estratégias - Recomendações e Projeções
"""
import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Adicionar path para imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_processed_data, get_top_countries, filter_by_year_range
from utils.data_processing import calculate_cagr, identify_growing_markets
from utils.visualizations import COLORS
import plotly.graph_objects as go
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Estratégias - Wine Export Analysis",
    page_icon="🎯",
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
    .strategy-box {
        background-color: #d4edda;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .action-box {
        background-color: #e7f3ff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E8B57;
        margin: 1rem 0;
    }
    .kpi-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="big-title">🎯 Estratégias: Transformando o Futuro</p>', unsafe_allow_html=True)
st.markdown("### *Recomendações acionáveis baseadas em dados para investidores e acionistas*")
st.markdown("---")

# Carregar dados
df_export, df_import, df_comparacao = load_processed_data()

# Storytelling: Introdução
st.markdown("""
## 🚀 A Jornada de Transformação

Vimos o **diagnóstico** (onde estamos) e o **contexto** (por que estamos assim). 
Agora é hora de traçar o **caminho para o futuro**: como transformar o Brasil de um exportador 
de volume/baixo valor em um **player relevante no mercado premium internacional**.
""")

st.markdown("---")

# Seção 1: Mercados com Potencial de Crescimento
st.markdown('<p class="section-title">📈 Oportunidade 1: Mercados Emergentes</p>', unsafe_allow_html=True)

st.markdown("""
### 🎯 Identificação de Mercados Promissores

Analisamos o **crescimento histórico** (CAGR - Taxa de Crescimento Anual Composta) 
de cada mercado para identificar países com **trajetória ascendente**.
""")

# Identificar mercados em crescimento
growing_markets = identify_growing_markets(df_export, min_years=5, min_cagr=5)

if len(growing_markets) > 0:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Gráfico de barras - CAGR por país
        fig_cagr = go.Figure()
        
        top_growing = growing_markets.head(10)
        
        fig_cagr.add_trace(go.Bar(
            x=top_growing['cagr_valor'],
            y=top_growing['pais'],
            orientation='h',
            marker=dict(
                color=top_growing['cagr_valor'],
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="CAGR (%)")
            ),
            text=top_growing['cagr_valor'].round(1),
            texttemplate='%{text}%',
            textposition='outside'
        ))
        
        fig_cagr.update_layout(
            title="Top 10 Mercados com Maior Crescimento (CAGR Valor)",
            xaxis_title="CAGR (%)",
            template='plotly_white',
            height=500
        )
        
        st.plotly_chart(fig_cagr, use_container_width=True)
    
    with col2:
        st.markdown("""
        ### 🌟 Destaques
        
        Países com **crescimento consistente** 
        nas exportações brasileiras:
        
        **Critérios:**
        - CAGR ≥ 5% ao ano
        - Mínimo 5 anos de dados
        - Base de volume relevante
        
        **Oportunidade:**
        Mercados que já **conhecem** 
        nossos vinhos e estão 
        **aumentando** o consumo.
        """)

# Tabela de mercados promissores
st.markdown("### 📋 Análise Detalhada - Mercados com Potencial")

if len(growing_markets) > 0:
    growing_display = growing_markets.head(10).copy()
    growing_display['cagr_valor'] = growing_display['cagr_valor'].apply(lambda x: f"{x:.1f}%")
    growing_display['cagr_volume'] = growing_display['cagr_volume'].apply(lambda x: f"{x:.1f}%")
    growing_display['total_valor_usd'] = growing_display['total_valor_usd'].apply(lambda x: f"US$ {x:,.0f}")
    growing_display['total_litros'] = growing_display['total_litros'].apply(lambda x: f"{x:,.0f}")
    
    growing_display.columns = ['País', 'CAGR Valor', 'CAGR Volume', 'Valor Total', 'Volume Total', 'Anos']
    
    st.dataframe(growing_display, hide_index=True, use_container_width=True)

st.markdown("""
<div class="strategy-box">
<h4>💡 Recomendação Estratégica 1: Apostar em Mercados Emergentes</h4>
<ul>
    <li><strong>Foco:</strong> Países com CAGR >10% ao ano</li>
    <li><strong>Ação:</strong> Missões comerciais, participação em feiras, marketing direcionado</li>
    <li><strong>Meta:</strong> Dobrar participação nesses mercados em 3-5 anos</li>
    <li><strong>Investimento:</strong> Marketing, distribuição, certificações locais</li>
</ul>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Seção 2: Diversificação Geográfica
st.markdown('<p class="section-title">🌍 Oportunidade 2: Diversificação Geográfica</p>', unsafe_allow_html=True)

st.markdown("""
### 🎯 Reduzir Dependência do Paraguai

Atualmente, **70% das exportações** vão para um único país. Isso cria vulnerabilidade extrema.
""")

# Calcular participação atual
total_valor = df_export['valor_usd'].sum()
paraguay_valor = df_export[df_export['pais_destino'] == 'Paraguai']['valor_usd'].sum()
paraguay_pct = (paraguay_valor / total_valor) * 100

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="kpi-box">
    <h3 style="color: #8B0000; margin: 0;">🇵🇾 Paraguai</h3>
    <h2 style="color: #8B0000; margin: 0.5rem 0;">{paraguay_pct:.1f}%</h2>
    <p style="margin: 0; color: #666;">Participação Atual</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="kpi-box">
    <h3 style="color: #DAA520; margin: 0;">🎯 Meta 2030</h3>
    <h2 style="color: #DAA520; margin: 0.5rem 0;">40%</h2>
    <p style="margin: 0; color: #666;">Participação Alvo</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    reducao = paraguay_pct - 40
    st.markdown(f"""
    <div class="kpi-box">
    <h3 style="color: #28a745; margin: 0;">📉 Redução</h3>
    <h2 style="color: #28a745; margin: 0.5rem 0;">-{reducao:.1f}pp</h2>
    <p style="margin: 0; color: #666;">Pontos Percentuais</p>
    </div>
    """, unsafe_allow_html=True)

# Mercados prioritários para diversificação
st.markdown("### 🎯 Mercados Prioritários para Expansão")

target_markets = pd.DataFrame({
    'País': ['Estados Unidos', 'Reino Unido', 'China', 'Países Baixos', 'Alemanha'],
    'Potencial': ['Alto', 'Alto', 'Muito Alto', 'Médio', 'Médio'],
    'Razão': [
        'Maior mercado mundial, alta renda, consumo crescente',
        'Tradição em importação, valorização de novos produtores',
        'Mercado em explosão, classe média crescente',
        'Hub de distribuição para Europa',
        'Alto consumo per capita, mercado maduro'
    ],
    'Preço Alvo': ['US$ 4-6/L', 'US$ 5-7/L', 'US$ 3-5/L', 'US$ 4-5/L', 'US$ 4-6/L']
})

st.dataframe(target_markets, hide_index=True, use_container_width=True)

st.markdown("""
<div class="strategy-box">
<h4>💡 Recomendação Estratégica 2: Diversificação Agressiva</h4>
<ul>
    <li><strong>Meta:</strong> Reduzir participação do Paraguai para <40% até 2030</li>
    <li><strong>Ação:</strong> Entrada em 5 novos mercados prioritários</li>
    <li><strong>Investimento:</strong> Certificações internacionais (USDA Organic, EU Organic)</li>
    <li><strong>Parcerias:</strong> Distribuidores locais em cada mercado-alvo</li>
</ul>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Seção 3: Upgrade de Qualidade
st.markdown('<p class="section-title">⬆️ Oportunidade 3: Upgrade de Produto</p>', unsafe_allow_html=True)

st.markdown("""
### 💎 De Volume para Valor: Estratégia de Premium

Atualmente exportamos a **US$ 1.38/L**. Para competir globalmente, precisamos atingir **US$ 3.50-4.00/L**.
""")

# Comparação de preços
price_comparison = pd.DataFrame({
    'Categoria': ['Brasil (Atual)', 'Chile (Benchmark)', 'Argentina (Benchmark)', 'Portugal (Benchmark)', 'Meta Brasil 2030'],
    'Preço Médio': [1.38, 2.79, 3.32, 3.07, 3.75],
    'Posicionamento': ['Vinho de Mesa', 'Fino/Premium', 'Fino/Premium', 'Fino/Premium', 'Fino/Premium']
})

fig_price_comp = go.Figure()

colors_map = {
    'Brasil (Atual)': COLORS['warning'],
    'Chile (Benchmark)': COLORS['accent'],
    'Argentina (Benchmark)': COLORS['accent'],
    'Portugal (Benchmark)': COLORS['accent'],
    'Meta Brasil 2030': COLORS['success']
}

fig_price_comp.add_trace(go.Bar(
    x=price_comparison['Categoria'],
    y=price_comparison['Preço Médio'],
    marker_color=[colors_map[cat] for cat in price_comparison['Categoria']],
    text=price_comparison['Preço Médio'],
    texttemplate='US$ %{text:.2f}/L',
    textposition='outside'
))

fig_price_comp.update_layout(
    title="Comparação de Preço Médio: Brasil vs Concorrentes",
    yaxis_title="Preço Médio (USD/L)",
    template='plotly_white',
    height=500,
    showlegend=False
)

st.plotly_chart(fig_price_comp, use_container_width=True)

# Estratégia de portfólio
st.markdown("### 🍷 Estratégia de Portfólio")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### 📦 Portfólio Atual
    
    **Vinho de Mesa: 85%**
    - Baixo valor agregado
    - Mercado de volume
    - Preço: US$ 1-2/L
    
    **Vinho Fino: 10%**
    - Qualidade média
    - Exportação limitada
    - Preço: US$ 2-3/L
    
    **Espumantes: 5%**
    - Potencial não explorado
    - Qualidade reconhecida
    - Preço: US$ 3-5/L
    """)

with col2:
    st.markdown("""
    #### 🎯 Portfólio Alvo 2030
    
    **Vinho de Mesa: 50%**
    - Manter mercados estabelecidos
    - Melhorar qualidade
    - Preço: US$ 1.50-2.50/L
    
    **Vinho Fino: 35%**
    - Foco principal expansão
    - Vale dos Vinhedos
    - Preço: US$ 3.50-5/L
    
    **Espumantes: 15%**
    - Crescimento acelerado
    - Marketing premium
    - Preço: US$ 5-8/L
    """)

st.markdown("""
<div class="strategy-box">
<h4>💡 Recomendação Estratégica 3: Transformação de Portfólio</h4>
<ul>
    <li><strong>Meta de Preço:</strong> Atingir US$ 3.75/L médio até 2030 (+171%)</li>
    <li><strong>Foco:</strong> Vinhos finos de regiões reconhecidas (Vale dos Vinhedos, Serra Gaúcha)</li>
    <li><strong>Diferenciação:</strong> Vinhos orgânicos, biodinâmicos, safras limitadas</li>
    <li><strong>Investimento:</strong> Tecnologia de vinificação, marketing de origem</li>
</ul>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Seção 4: Projeções
st.markdown('<p class="section-title">📊 Projeções 2025-2030</p>', unsafe_allow_html=True)

st.markdown("""
### 🔮 Cenários Futuros

Com base nas estratégias propostas, projetamos três cenários possíveis:
""")

# Criar projeções
years_proj = np.array([2024, 2025, 2026, 2027, 2028, 2029, 2030])

# Cenário conservador (manter tendência atual)
valor_2023 = df_comparacao[df_comparacao['ano'] == 2023]['exp_usd'].values[0]
conservador = valor_2023 * np.array([1.0, 0.98, 0.97, 0.96, 0.95, 0.94, 0.93])

# Cenário moderado (implementação parcial)
moderado = valor_2023 * np.array([1.0, 1.05, 1.12, 1.20, 1.30, 1.42, 1.55])

# Cenário otimista (implementação completa)
otimista = valor_2023 * np.array([1.0, 1.10, 1.25, 1.45, 1.70, 2.00, 2.35])

fig_proj = go.Figure()

fig_proj.add_trace(go.Scatter(
    x=years_proj,
    y=conservador / 1_000_000,
    name='Conservador (Inércia)',
    line=dict(color=COLORS['warning'], width=2, dash='dash'),
    mode='lines+markers'
))

fig_proj.add_trace(go.Scatter(
    x=years_proj,
    y=moderado / 1_000_000,
    name='Moderado (Implementação Parcial)',
    line=dict(color=COLORS['secondary'], width=3),
    mode='lines+markers'
))

fig_proj.add_trace(go.Scatter(
    x=years_proj,
    y=otimista / 1_000_000,
    name='Otimista (Implementação Completa)',
    line=dict(color=COLORS['success'], width=3),
    mode='lines+markers'
))

fig_proj.update_layout(
    title="Projeção de Valor de Exportações (2024-2030)",
    xaxis_title="Ano",
    yaxis_title="Valor (Milhões USD)",
    template='plotly_white',
    height=500,
    hovermode='x unified'
)

st.plotly_chart(fig_proj, use_container_width=True)

# Tabela de cenários
st.markdown("### 📋 Comparação de Cenários - 2030")

cenarios_2030 = pd.DataFrame({
    'Cenário': ['Conservador', 'Moderado', 'Otimista'],
    'Valor Exportação': [
        f"US$ {conservador[-1]/1_000_000:.0f}M",
        f"US$ {moderado[-1]/1_000_000:.0f}M",
        f"US$ {otimista[-1]/1_000_000:.0f}M"
    ],
    'Crescimento vs 2023': [
        f"{((conservador[-1]/valor_2023 - 1) * 100):.0f}%",
        f"+{((moderado[-1]/valor_2023 - 1) * 100):.0f}%",
        f"+{((otimista[-1]/valor_2023 - 1) * 100):.0f}%"
    ],
    'Preço Médio Alvo': ['US$ 1.50/L', 'US$ 2.50/L', 'US$ 4.00/L'],
    'Novos Mercados': ['0-1', '3-4', '5+'],
    'Investimento Necessário': ['Baixo', 'Médio', 'Alto']
})

st.dataframe(cenarios_2030, hide_index=True, use_container_width=True)

st.markdown("---")

# Seção 5: Plano de Ação
st.markdown('<p class="section-title">🗓️ Plano de Ação: Roadmap 2025-2030</p>', unsafe_allow_html=True)

timeline = pd.DataFrame({
    'Período': ['2025', '2026-2027', '2028-2029', '2030'],
    'Ações Prioritárias': [
        '• Certificações internacionais\n• Missões comerciais (EUA, UK, China)\n• Lançamento linha premium',
        '• Entrada em 3 novos mercados\n• Upgrade de vinícolas\n• Campanha marketing internacional',
        '• Expansão para 5+ mercados\n• Consolidação marca premium\n• Parcerias estratégicas distribuidores',
        '• Avaliação de resultados\n• Ajuste de estratégia\n• Planejamento próxima década'
    ],
    'Investimento Estimado': ['US$ 2-3M', 'US$ 5-8M', 'US$ 8-12M', 'US$ 3-5M']
})

for idx, row in timeline.iterrows():
    with st.expander(f"📅 **{row['Período']}** - {row['Investimento Estimado']}"):
        st.markdown(row['Ações Prioritárias'])

st.markdown("---")

# Seção 6: KPIs e Acompanhamento
st.markdown('<p class="section-title">📈 KPIs para Acompanhamento</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 📊 KPIs Operacionais
    
    **Volume e Valor:**
    - Volume exportado (litros)
    - Valor exportado (USD)
    - Preço médio (USD/L)
    - Crescimento YoY (%)
    
    **Mercados:**
    - Número de países ativos
    - Participação do Paraguai (%)
    - Novos mercados/ano
    - Taxa de retenção de clientes
    
    **Portfólio:**
    - % Vinhos finos
    - % Espumantes
    - % Orgânicos
    - Mix de produtos
    """)

with col2:
    st.markdown("""
    ### 🎯 KPIs Estratégicos
    
    **Competitividade:**
    - Preço médio vs benchmarks
    - Share of wallet em mercados-chave
    - Ranking em competições internacionais
    - NPS (Net Promoter Score)
    
    **Rentabilidade:**
    - Margem bruta (%)
    - ROI de marketing
    - CAC (Custo Aquisição Cliente)
    - LTV (Lifetime Value)
    
    **Sustentabilidade:**
    - Hectares orgânicos
    - Certificações obtidas
    - Pegada de carbono
    - Práticas sustentáveis
    """)

st.markdown("---")

# Conclusão Final
st.markdown('<p class="section-title">🎓 Conclusões e Recomendações Finais</p>', unsafe_allow_html=True)

st.markdown("""
## 📝 Síntese Executiva para Investidores

### ✅ O Que Sabemos
1. **Brasil tem potencial não explorado** no mercado internacional de vinhos
2. **Concentração extrema** (70% Paraguai) cria vulnerabilidade
3. **Posicionamento de baixo valor** (US$ 1.38/L) limita crescimento
4. **Déficit comercial** de US$ 6+ bilhões em 15 anos

### 🎯 Para Onde Ir
1. **Diversificação geográfica:** Reduzir Paraguai para <40%
2. **Upgrade de qualidade:** Atingir US$ 3.75/L médio
3. **Novos mercados:** EUA, Reino Unido, China como prioritários
4. **Transformação de portfólio:** Mais vinhos finos e espumantes

### 💰 Retorno Esperado
- **Cenário Moderado:** +55% em valor até 2030
- **Cenário Otimista:** +135% em valor até 2030
- **Payback:** 3-5 anos com implementação consistente

### 🚀 Próximos Passos Imediatos
1. **Formar comitê estratégico** de exportação
2. **Contratar consultoria** de mercado internacional
3. **Iniciar certificações** (Organic, Kosher, Halal)
4. **Planejar missões comerciais** para 2025

---

## 🌟 Mensagem Final

O Brasil tem **todos os ingredientes** para se tornar um player relevante no mercado internacional de vinhos premium:

✅ **Base produtiva** estabelecida  
✅ **Know-how** em vinicultura  
✅ **Regiões reconhecidas** (Vale dos Vinhedos)  
✅ **Mercado interno** forte e sofisticado  

O que falta é **estratégia**, **foco** e **investimento direcionado**.

Com as recomendações apresentadas nesta análise, **é possível transformar o setor vitivinícola 
brasileiro de exportador marginal em competidor global**, gerando valor para produtores, 
investidores e para o país.

---

**O futuro do vinho brasileiro no mundo está em nossas mãos. É hora de agir! 🍷**
""")

st.markdown("---")

# Footer
st.success("✅ **Análise completa!** Utilize este relatório como base para decisões estratégicas e apresentações a investidores.")

st.info("""
📧 **Contato:** Para dúvidas ou discussões sobre as estratégias propostas, entre em contato com o autor do projeto.

📊 **Fontes:** Todas as análises são baseadas em dados oficiais da EMBRAPA Vitibrasil (2009-2023).

🔄 **Atualização:** Recomenda-se revisar estas estratégias anualmente com dados atualizados.
""")