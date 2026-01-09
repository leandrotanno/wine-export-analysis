# 🍷 Exportações Brasileiras de Vinho: Análise Estratégica

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12.12-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.39.0-red?style=for-the-badge&logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-2.2.3-150458?style=for-the-badge&logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-5.24.1-3F4F75?style=for-the-badge&logo=plotly)

**Análise estratégica das exportações brasileiras de vinho (2009-2023)**

[📊 Ver Demo](#) • [📖 Documentação](#estrutura-do-projeto) • [🚀 Quick Start](#-quick-start)

</div>

---

## 📋 Sobre o Projeto

Este projeto foi desenvolvido como parte do **Tech Challenge - Fase 1** do curso de **Data Analytics da POSTECH**, com o objetivo de analisar 15 anos de dados das exportações brasileiras de vinho e propor estratégias para transformar o Brasil em um player relevante no mercado internacional de vinhos premium.

### 🎯 Pergunta Norteadora

> **"Como o Brasil pode evoluir de um modelo de exportação de volume/baixo valor para um posicionamento competitivo no mercado internacional de vinhos premium?"**

### 🔍 Principais Descobertas

- 🇵🇾 **Concentração extrema**: 70% das exportações vão para o Paraguai
- 💰 **Baixo valor agregado**: Preço médio de US$ 1.38/L (vinho de mesa)
- 📉 **Balança negativa**: Déficit acumulado de US$ 6+ bilhões (2009-2023)
- 🌍 **Oportunidades**: EUA, Reino Unido e China como mercados prioritários

---

## 🚀 Quick Start

### Pré-requisitos

- Python 3.12+
- pip
- virtualenv (opcional, mas recomendado)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/wine-export-analysis.git
cd wine-export-analysis

# Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt

# Processe os dados (primeira vez)
python utils/data_processing.py
```

### Executar a aplicação

```bash
streamlit run app.py
```

A aplicação será aberta automaticamente no navegador em `http://localhost:8501`

---

## 📊 Estrutura do Projeto

```
wine-export-analysis/
│
├── app.py                      # Página inicial
├── requirements.txt            # Dependências do projeto
├── README.md                   # Este arquivo
│
├── .streamlit/
│   └── config.toml            # Configurações do Streamlit (tema)
│
├── data/
│   ├── raw/                   # Dados brutos da Embrapa
│   │   ├── Exportacao.csv
│   │   ├── Importacao.csv
│   │   ├── Producao.csv
│   │   ├── Processamento.csv
│   │   └── Comercializacao.csv
│   └── processed/             # Dados processados
│       ├── export_processed.csv
│       ├── import_processed.csv
│       └── comparacao_exp_imp.csv
│
├── pages/                     # Páginas do Streamlit
│   ├── 1_Diagnostico.py      # Análise da situação atual
│   ├── 2_Contexto.py         # Análise comparativa e estrutural
│   └── 3_Estrategias.py      # Recomendações e projeções
│
└── utils/                     # Módulos auxiliares
    ├── __init__.py
    ├── data_loader.py         # Funções de carregamento
    ├── data_processing.py     # Processamento de dados
    └── visualizations.py      # Gráficos com Plotly
```

---

## 📈 Funcionalidades

### 🏠 Página Inicial
- Visão geral do projeto e pergunta norteadora
- Métricas principais (2009-2023)
- KPIs gerais de exportação e importação
- Principais insights identificados

### 📊 Diagnóstico
- Evolução temporal das exportações (volume e valor)
- Análise comparativa: Exportação vs Importação
- Concentração de mercado (Índice HHI)
- Top 15 países destino
- Matriz de dependência do Paraguai

### 🔍 Contexto
- Análise de preços: Export vs Import
- Identificação dos principais concorrentes
- Segmentação por faixa de preço
- Matriz: Preço médio vs Volume por país
- Balança comercial detalhada
- Análise de fatores estruturais

### 🎯 Estratégias
- Identificação de mercados emergentes (CAGR)
- Estratégia de diversificação geográfica
- Plano de upgrade de portfólio (premium)
- Projeções 2025-2030 (3 cenários)
- Roadmap de implementação
- KPIs de acompanhamento

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Python** | 3.12.12 | Linguagem principal |
| **Streamlit** | 1.39.0 | Framework web para dashboards |
| **Pandas** | 2.2.3 | Manipulação e análise de dados |
| **Plotly** | 5.24.1 | Visualizações interativas |
| **NumPy** | 2.1.3 | Computação numérica |
| **SciPy** | 1.14.1 | Análises estatísticas |

---

## 📊 Fonte dos Dados

**Origem:** EMBRAPA Vitibrasil  
**URL:** http://vitibrasil.cnpuv.embrapa.br  
**Período:** 2009-2023 (15 anos)  
**Datasets utilizados:**
- Exportação (137 países)
- Importação (68 países)
- Produção (categorias de vinhos)
- Processamento (cultivares)
- Comercialização (mercado interno)

**Conversão aplicada:** 1 kg = 1 litro (conforme especificação do projeto)

---

## 📝 Metodologia

### 1. Coleta de Dados
Extração de dados históricos da plataforma Embrapa Vitibrasil, cobrindo o período de 2009 a 2023.

### 2. Processamento
Transformação dos dados de formato wide para long, limpeza, tratamento de valores faltantes e criação de métricas derivadas.

### 3. Análise Exploratória
- Análise de tendências temporais
- Identificação de padrões e outliers
- Cálculo de métricas de concentração (HHI)
- Análise de crescimento (CAGR)

### 4. Visualização
Criação de dashboards interativos com Plotly, incluindo:
- Gráficos de linha (evolução temporal)
- Treemaps (distribuição por país)
- Scatter plots (preço vs volume)
- Gráficos de barras (comparações)
- Gráficos de pizza (concentração)

### 5. Geração de Insights
Análise estratégica com foco em:
- Identificação de oportunidades
- Análise competitiva
- Recomendações acionáveis
- Projeções futuras

---

## 🎨 Design e UX

### Paleta de Cores
- **Primary:** `#8B0000` (Vinho tinto)
- **Secondary:** `#DAA520` (Dourado)
- **Accent:** `#2E8B57` (Verde uvas)
- **Neutral:** `#4A4A4A` (Grafite)

### Princípios de Design
- **Storytelling em 3 atos**: Diagnóstico → Contexto → Estratégias
- **Visualizações interativas**: Todos os gráficos com hover e zoom
- **Responsividade**: Layout adaptável para diferentes tamanhos de tela
- **Acessibilidade**: Cores e fontes com bom contraste

---

## 📚 Documentação Adicional

- [GUIA_DE_USO.md](GUIA_DE_USO.md) - Instruções detalhadas de uso

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais como parte do Tech Challenge da POSTECH.

---

## 👨‍💻 Autor

**Tanno**  
Senior Data Analyst | POSTECH Data Analytics

---

## 🙏 Agradecimentos

- **POSTECH** - Pela oportunidade e estrutura do curso
- **EMBRAPA Vitibrasil** - Pelos dados públicos disponibilizados
- **Comunidade Streamlit** - Pela excelente ferramenta de visualização

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela!**

Desenvolvido com ☕ e 🍷 para o Tech Challenge - POSTECH Data Analytics

</div>