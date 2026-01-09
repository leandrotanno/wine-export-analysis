"""
Funções para processar dados brutos da Embrapa Vitibrasil
"""
import pandas as pd
import numpy as np
from pathlib import Path


def process_export_data(df_raw, year_start=2009, year_end=2023):
    """
    Transforma dados de exportação de formato wide para long.
    
    Estrutura original: País | 1970 (kg) | 1970.1 (USD) | 1971 (kg) | 1971.1 (USD) ...
    Estrutura final: país_destino | ano | quantidade_kg | valor_usd | quantidade_litros | preco_medio
    
    Args:
        df_raw: DataFrame bruto de exportação
        year_start: Ano inicial para filtrar
        year_end: Ano final para filtrar
        
    Returns:
        DataFrame: Dados processados
    """
    data_export = []
    
    for _, row in df_raw.iterrows():
        pais = row['País']
        
        # Iterar pelas colunas de anos (pulando .1 que são valores USD)
        for i in range(2, len(df_raw.columns), 2):
            ano_col = df_raw.columns[i]
            
            if '.' in ano_col:  # Pular colunas .1
                continue
            
            try:
                ano = int(ano_col)
                kg = row[ano_col]
                valor_usd = row[f"{ano_col}.1"]
                
                # Filtrar apenas registros com valores válidos
                if pd.notna(kg) and pd.notna(valor_usd) and kg > 0 and valor_usd > 0:
                    data_export.append({
                        'pais_destino': pais,
                        'ano': ano,
                        'quantidade_kg': int(kg),
                        'valor_usd': float(valor_usd)
                    })
            except (ValueError, KeyError):
                continue
    
    df_export = pd.DataFrame(data_export)
    
    # Adicionar coluna de litros (1kg = 1L conforme enunciado)
    df_export['quantidade_litros'] = df_export['quantidade_kg']
    
    # Calcular preço médio
    df_export['preco_medio_usd_litro'] = df_export['valor_usd'] / df_export['quantidade_litros']
    
    # Filtrar por anos
    df_export = df_export[(df_export['ano'] >= year_start) & (df_export['ano'] <= year_end)]
    
    return df_export


def process_import_data(df_raw, year_start=2009, year_end=2023):
    """
    Transforma dados de importação (mesma estrutura que exportação).
    
    Args:
        df_raw: DataFrame bruto de importação
        year_start: Ano inicial
        year_end: Ano final
        
    Returns:
        DataFrame: Dados processados
    """
    data_import = []
    
    for _, row in df_raw.iterrows():
        pais = row['País']
        
        for i in range(2, len(df_raw.columns), 2):
            ano_col = df_raw.columns[i]
            
            if '.' in ano_col:
                continue
            
            try:
                ano = int(ano_col)
                kg = row[ano_col]
                valor_usd = row[f"{ano_col}.1"]
                
                if pd.notna(kg) and pd.notna(valor_usd) and kg > 0 and valor_usd > 0:
                    data_import.append({
                        'pais_origem': pais,
                        'ano': ano,
                        'quantidade_kg': int(kg),
                        'valor_usd': float(valor_usd)
                    })
            except (ValueError, KeyError):
                continue
    
    df_import = pd.DataFrame(data_import)
    df_import['quantidade_litros'] = df_import['quantidade_kg']
    df_import['preco_medio_usd_litro'] = df_import['valor_usd'] / df_import['quantidade_litros']
    
    df_import = df_import[(df_import['ano'] >= year_start) & (df_import['ano'] <= year_end)]
    
    return df_import


def create_comparison_table(df_export, df_import):
    """
    Cria tabela comparativa entre exportação e importação por ano.
    
    Args:
        df_export: DataFrame de exportações processado
        df_import: DataFrame de importações processado
        
    Returns:
        DataFrame: Tabela comparativa
    """
    # Agregação por ano - Exportação
    export_yearly = df_export.groupby('ano').agg({
        'quantidade_litros': 'sum',
        'valor_usd': 'sum'
    }).reset_index()
    export_yearly.columns = ['ano', 'exp_litros', 'exp_usd']
    
    # Agregação por ano - Importação
    import_yearly = df_import.groupby('ano').agg({
        'quantidade_litros': 'sum',
        'valor_usd': 'sum'
    }).reset_index()
    import_yearly.columns = ['ano', 'imp_litros', 'imp_usd']
    
    # Merge
    comparacao = export_yearly.merge(import_yearly, on='ano', how='outer').fillna(0)
    
    # Calcular balanças
    comparacao['balanca_litros'] = comparacao['exp_litros'] - comparacao['imp_litros']
    comparacao['balanca_usd'] = comparacao['exp_usd'] - comparacao['imp_usd']
    
    # Preços médios
    comparacao['preco_medio_exp'] = comparacao['exp_usd'] / comparacao['exp_litros']
    comparacao['preco_medio_imp'] = comparacao['imp_usd'] / comparacao['imp_litros']
    
    # Diferença percentual de preços
    comparacao['diferenca_preco_pct'] = (
        (comparacao['preco_medio_imp'] / comparacao['preco_medio_exp'] - 1) * 100
    )
    
    return comparacao


def calculate_cagr(df, value_col, year_col='ano'):
    """
    Calcula CAGR (Compound Annual Growth Rate) para uma série temporal.
    
    Args:
        df: DataFrame com dados temporais
        value_col: Nome da coluna de valores
        year_col: Nome da coluna de anos
        
    Returns:
        float: CAGR em percentual
    """
    df_sorted = df.sort_values(year_col)
    
    initial_value = df_sorted[value_col].iloc[0]
    final_value = df_sorted[value_col].iloc[-1]
    num_years = df_sorted[year_col].iloc[-1] - df_sorted[year_col].iloc[0]
    
    if initial_value == 0 or num_years == 0:
        return 0
    
    cagr = (np.power(final_value / initial_value, 1 / num_years) - 1) * 100
    
    return cagr


def identify_growing_markets(df_export, min_years=5, min_cagr=5):
    """
    Identifica mercados com crescimento consistente.
    
    Args:
        df_export: DataFrame de exportações
        min_years: Mínimo de anos com dados
        min_cagr: CAGR mínimo para considerar (%)
        
    Returns:
        DataFrame: Países com crescimento identificado
    """
    growing_markets = []
    
    for pais in df_export['pais_destino'].unique():
        df_pais = df_export[df_export['pais_destino'] == pais].copy()
        
        # Filtrar países com dados suficientes
        if len(df_pais) < min_years:
            continue
        
        # Calcular CAGR
        cagr_valor = calculate_cagr(df_pais, 'valor_usd')
        cagr_volume = calculate_cagr(df_pais, 'quantidade_litros')
        
        if cagr_valor >= min_cagr:
            total_valor = df_pais['valor_usd'].sum()
            total_litros = df_pais['quantidade_litros'].sum()
            
            growing_markets.append({
                'pais': pais,
                'cagr_valor': cagr_valor,
                'cagr_volume': cagr_volume,
                'total_valor_usd': total_valor,
                'total_litros': total_litros,
                'anos_dados': len(df_pais)
            })
    
    df_growing = pd.DataFrame(growing_markets)
    df_growing = df_growing.sort_values('cagr_valor', ascending=False)
    
    return df_growing


def segment_countries_by_price(df_export, low_threshold=1.5, high_threshold=3.0):
    """
    Segmenta países por faixa de preço médio.
    
    Args:
        df_export: DataFrame de exportações
        low_threshold: Limite inferior (USD/L)
        high_threshold: Limite superior (USD/L)
        
    Returns:
        dict: Países segmentados por faixa
    """
    pais_preco = df_export.groupby('pais_destino').agg({
        'valor_usd': 'sum',
        'quantidade_litros': 'sum'
    }).reset_index()
    
    pais_preco['preco_medio'] = pais_preco['valor_usd'] / pais_preco['quantidade_litros']
    
    segments = {
        'baixo': pais_preco[pais_preco['preco_medio'] < low_threshold]['pais_destino'].tolist(),
        'medio': pais_preco[
            (pais_preco['preco_medio'] >= low_threshold) & 
            (pais_preco['preco_medio'] < high_threshold)
        ]['pais_destino'].tolist(),
        'alto': pais_preco[pais_preco['preco_medio'] >= high_threshold]['pais_destino'].tolist()
    }
    
    return segments, pais_preco


def process_all_data(data_path='data/raw', output_path='data/processed'):
    """
    Processa todos os dados brutos e salva versões processadas.
    Execute este script uma vez antes de rodar o Streamlit.
    
    Args:
        data_path: Caminho dos dados brutos
        output_path: Caminho para salvar dados processados
    """
    from pathlib import Path
    
    data_path = Path(data_path)
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print("🔄 Processando dados...")
    
    # Carregar dados brutos
    df_exp_raw = pd.read_csv(data_path / 'Exportacao.csv', sep=';')
    df_imp_raw = pd.read_csv(data_path / 'Importacao.csv', sep=';')
    
    # Processar
    df_export = process_export_data(df_exp_raw)
    df_import = process_import_data(df_imp_raw)
    df_comparacao = create_comparison_table(df_export, df_import)
    
    # Salvar
    df_export.to_csv(output_path / 'export_processed.csv', index=False)
    df_import.to_csv(output_path / 'import_processed.csv', index=False)
    df_comparacao.to_csv(output_path / 'comparacao_exp_imp.csv', index=False)
    
    print(f"✅ Dados processados salvos em {output_path}/")
    print(f"   - export_processed.csv: {len(df_export)} registros")
    print(f"   - import_processed.csv: {len(df_import)} registros")
    print(f"   - comparacao_exp_imp.csv: {len(df_comparacao)} registros")


if __name__ == '__main__':
    # Executar processamento se rodado diretamente
    process_all_data()