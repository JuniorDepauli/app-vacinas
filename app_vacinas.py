
# app_vacinas.py
import streamlit as st
import pandas as pd

# Configuração do visual do app
st.set_page_config(
    page_title="Calendário de Vacinação",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tema escuro com CSS customizado
st.markdown(
    """
    <style>
    body {
        background-color: #121212;
        color: #ffffff;
    }
    .stApp {
        background-color: #1E1E1E;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Carregar dados
@st.cache_data
def carregar_dados():
    df = pd.read_excel("VacinasHum.xlsx", sheet_name="VACINAS")
    df = df.fillna("")
    
    # Remover colunas sem nome (como Unnamed: 0, etc.)
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    
    return df

df = carregar_dados()

# Título
st.title("💉 Consulta Interativa - Calendário de Vacinação")

# Filtros
st.sidebar.header("🔍 Filtros")

# Filtro por Classificação
st.sidebar.subheader("Filtrar por Classificação:")
filtro_class = []
for classificacao in df["NM_CLASSIFICAÇÃO"].unique():
    if st.sidebar.checkbox(classificacao, value=True):
        filtro_class.append(classificacao)

# Filtro por Vacina
st.sidebar.subheader("Filtrar por Vacina:")
filtro_vacina = st.sidebar.multiselect(
    "Filtrar por Vacina:", 
    df["VACINA"].unique(), 
    default=df["VACINA"].unique()
)

# Aplicar filtros
df_filtrado = df[
    (df["NM_CLASSIFICAÇÃO"].isin(filtro_class)) &
    (df["VACINA"].isin(filtro_vacina))
]

# Remover colunas da exibição final
colunas_ocultas = ["NU_CLASSIFICAÇÃO", "NM_CLASSIFICAÇÃO"]
df_exibicao = df_filtrado.drop(columns=[col for col in colunas_ocultas if col in df_filtrado.columns])

# KPIs simples
st.subheader("📊 INFORMAÇÕES")
col1, col2 = st.columns(2)
col1.metric("Vacinas Listadas", len(df_filtrado))
col2.metric("Classificações", df_filtrado["NM_CLASSIFICAÇÃO"].nunique())

# Tabela de visualização (agora com colunas ocultas)
st.subheader("📋 Detalhamento das Vacinas")
st.dataframe(df_exibicao.style.set_properties(**{
    'background-color': '#1E1E1E',
    'color': 'white'
}), use_container_width=True)

# Rodapé
st.markdown("---")
st.caption("Desenvolvido por Junior Depauli • Dados informativos baseados no Calendário de Vacinação - https://www.gov.br/saude/pt-br/vacinacao/calendario.")
