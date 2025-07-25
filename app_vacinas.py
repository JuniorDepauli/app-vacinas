
# app_vacinas.py
import streamlit as st
import pandas as pd

# Configuração do visual do app
st.set_page_config(
    page_title="Vacinas para Humanos",
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
    df = df.fillna("Não informado")
    return df

df = carregar_dados()

# Título
st.title("💉 Consulta Interativa - Vacinas para Humanos")

# Filtros
st.sidebar.header("🔍 Filtros")

# Filtro por Classificação
st.sidebar.subheader("Filtrar por Classificação:")
filtro_class = []
for classificacao in df["NM_CLASSIFICAÇÃO"].unique():
    if st.sidebar.checkbox(classificacao, value=True):  # value=True para selecionar por padrão
        filtro_class.append(classificacao)

# Filtro por Vacina
st.sidebar.subheader("Filtrar por Vacina:")
filtro_vacina = []
for vacina in df["VACINA"].unique():
    if st.sidebar.checkbox(vacina, value=True):  # value=True para selecionar por padrão
        filtro_vacina.append(vacina)

# Aplicar filtros
df_filtrado = df[
    (df["NM_CLASSIFICAÇÃO"].isin(filtro_class)) &
    (df["VACINA"].isin(filtro_vacina))
]

# KPIs simples
st.subheader("📊 INFORMAÇÕES")
col1, col2 = st.columns(2)
col1.metric("Vacinas Listadas", len(df_filtrado))
col2.metric("Classificação", df_filtrado["NM_CLASSIFICAÇÃO"].nunique())

# Tabela de visualização
st.subheader("📋 Detalhamento das Vacinas")
st.dataframe(df_filtrado.style.set_properties(**{
    'background-color': '#1E1E1E',
    'color': 'white'
}), use_container_width=True)

# Rodapé
st.markdown("---")
st.caption("Desenvolvido por Juninho • Dados informativos baseados no Calendário Nacional de Vacinação SUS.")
