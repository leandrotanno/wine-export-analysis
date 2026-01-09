"""
Funções para carregar e validar dados do projeto Wine Export Analysis
"""
import pandas as pd
from pathlib import Path
import streamlit as st


@st.cache_data
def load_processed_data():
    """
    Carrega dados já processados de exportação, importação e comparação.
    Usa cache do Streamlit para otimizar performance.
    
    Returns:
        tuple: (df_export, df_import, df_comparacao)
    """
    data_path = Path(__file__).parent.parent / 'data' / 'processed'
    
    try:
        df_export = pd.read_csv(data_path / 'export_processed.csv')
        df_import = pd.read_csv(data_path / 'import_processed.csv')
        df_comparacao = pd.read_csv(data_path / 'comparacao_exp_imp.csv')
        
        return df_export, df_import, df_comparacao
    
    except FileNotFoundError as e:
        st.error(f"❌ Erro ao carregar dados processados: {e}")
        st.info("💡 Execute o script de processamento primeiro!")
        st.stop()


@st.cache_data
def load_raw_data():
    """
    Carrega dados brutos dos CSVs originais da Embrapa.
    
    Returns:
        dict: Dicionário com os 5 dataframes
    """
    data_path = Path(__file__).parent.parent / 'data' / 'raw'
    
    datasets = {}
    
    try:
        # Exportação e Importação (sep=';')
        datasets['exportacao'] = pd.read_csv(data_path / 'Exportacao.csv', sep=';')
        datasets['importacao'] = pd.read_csv(data_path / 'Importacao.csv', sep=';')
        
        # Comercialização (sep=';')
        datasets['comercializacao'] = pd.read_csv(data_path / 'Comercializacao.csv', sep=';')
        
        # Produção e Processamento (sep='\t', formato especial)
        datasets['producao'] = pd.read_csv(data_path / 'Producao.csv', sep='\t', header=None)
        datasets['processamento'] = pd.read_csv(data_path / 'Processamento.csv', sep='\t', header=None)
        
        return datasets
    
    except FileNotFoundError as e:
        st.error(f"❌ Erro ao carregar dados brutos: {e}")
        st.info("💡 Verifique se os arquivos CSV estão em data/raw/")
        st.stop()


def get_export_summary(df_export):
    """
    Calcula estatísticas resumidas de exportação.
    
    Args:
        df_export: DataFrame de exportações processado
        
    Returns:
        dict: Dicionário com métricas principais
    """
    summary = {
        'total_litros': df_export['quantidade_litros'].sum(),
        'total_usd': df_export['valor_usd'].sum(),
        'preco_medio': df_export['valor_usd'].sum() / df_export['quantidade_litros'].sum(),
        'anos': df_export['ano'].nunique(),
        'paises': df_export['pais_destino'].nunique(),
        'ano_min': df_export['ano'].min(),
        'ano_max': df_export['ano'].max()
    }
    
    return summary


def get_top_countries(df_export, n=10, metric='valor_usd'):
    """
    Retorna top N países por uma métrica específica.
    
    Args:
        df_export: DataFrame de exportações
        n: Número de países
        metric: 'valor_usd' ou 'quantidade_litros'
        
    Returns:
        DataFrame: Top países ordenados
    """
    top = df_export.groupby('pais_destino').agg({
        'quantidade_litros': 'sum',
        'valor_usd': 'sum'
    }).reset_index()
    
    top['preco_medio'] = top['valor_usd'] / top['quantidade_litros']
    top = top.sort_values(metric, ascending=False).head(n)
    
    return top


def filter_by_year_range(df, year_start, year_end):
    """
    Filtra DataFrame por intervalo de anos.
    
    Args:
        df: DataFrame com coluna 'ano'
        year_start: Ano inicial
        year_end: Ano final
        
    Returns:
        DataFrame: Dados filtrados
    """
    return df[(df['ano'] >= year_start) & (df['ano'] <= year_end)].copy()


def calculate_market_concentration(df_export):
    """
    Calcula índice de concentração de mercado (Herfindahl-Hirschman Index).
    
    Args:
        df_export: DataFrame de exportações
        
    Returns:
        dict: Métricas de concentração
    """
    total_valor = df_export['valor_usd'].sum()
    
    # Market share por país
    market_share = df_export.groupby('pais_destino')['valor_usd'].sum() / total_valor
    
    # HHI (soma dos quadrados dos market shares)
    hhi = (market_share ** 2).sum() * 10000  # Multiplicado por 10000 (padrão)
    
    # Top 5 e Top 10 concentration
    top5 = market_share.nlargest(5).sum() * 100
    top10 = market_share.nlargest(10).sum() * 100
    
    return {
        'hhi': hhi,
        'top5_pct': top5,
        'top10_pct': top10,
        'interpretation': get_hhi_interpretation(hhi)
    }


def get_hhi_interpretation(hhi):
    """
    Interpreta o índice HHI.
    
    Args:
        hhi: Valor do HHI
        
    Returns:
        str: Interpretação
    """
    if hhi < 1500:
        return "Mercado não concentrado"
    elif hhi < 2500:
        return "Mercado moderadamente concentrado"
    else:
        return "Mercado altamente concentrado"


def get_yearly_trends(df_export):
    """
    Calcula tendências anuais de exportação.
    
    Args:
        df_export: DataFrame de exportações
        
    Returns:
        DataFrame: Agregação por ano
    """
    trends = df_export.groupby('ano').agg({
        'quantidade_litros': 'sum',
        'valor_usd': 'sum',
        'pais_destino': 'nunique'
    }).reset_index()
    
    trends.columns = ['ano', 'quantidade_litros', 'valor_usd', 'num_paises']
    trends['preco_medio'] = trends['valor_usd'] / trends['quantidade_litros']
    
    # Calcular crescimento YoY
    trends['crescimento_litros_pct'] = trends['quantidade_litros'].pct_change() * 100
    trends['crescimento_valor_pct'] = trends['valor_usd'].pct_change() * 100
    
    return trends