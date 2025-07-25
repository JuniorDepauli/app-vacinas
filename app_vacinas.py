
# app_vacinas.py
import streamlit as st
import pandas as pd

# Configuração do visual do app
st.set_page_config(
    page_title="Vacinas para Gestantes",
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
st.title("💉 Consulta Interativa - Vacinas para Gestantes")

# Filtros
st.sidebar.header("🔍 Filtros")
classificacoes = df["NM_CLASSIFICAÇÃO"].unique()
vacinas = df["VACINA"].unique()

filtro_class = st.sidebar.multiselect("Filtrar por Classificação:", classificacoes, default=classificacoes)
filtro_vacina = st.sidebar.multiselect("Filtrar por Vacina:", vacinas, default=vacinas)

df_filtrado = df[
    (df["NM_CLASSIFICAÇÃO"].isin(filtro_class)) &
    (df["VACINA"].isin(filtro_vacina))
]

# KPIs simples
st.subheader("📊 Resumo")
col1, col2 = st.columns(2)
col1.metric("Total de Vacinas Listadas", len(df_filtrado))
col2.metric("Tipos de Classificação", df_filtrado["NM_CLASSIFICAÇÃO"].nunique())

# Tabela de visualização
st.subheader("📋 Detalhamento das Vacinas")
st.dataframe(df_filtrado.style.set_properties(**{
    'background-color': '#1E1E1E',
    'color': 'white'
}), use_container_width=True)

# Rodapé
st.markdown("---")
st.caption("Desenvolvido por Juninho • Dados informativos baseados na planilha fornecida.")
