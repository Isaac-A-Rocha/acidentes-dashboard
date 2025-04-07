import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from dateutil import parser
import numpy as np

# === Funções de tratamento ===

@st.cache_data
def carregar_dados(caminho_csv):
    df = pd.read_csv(caminho_csv, sep=';')

    # Conversões e filtros
    df = df.dropna(subset=['latitude', 'longitude'])
    df[['latitude', 'longitude']] = df[['latitude', 'longitude']].astype(float)
    df = df[
        (df['latitude'] != 0) & (df['longitude'] != 0) &
        (df['latitude'].between(-30.30, -29.80)) &
        (df['longitude'].between(-51.40, -50.90))
    ]

    df['data'] = pd.to_datetime(df['data'], errors='coerce')
    df = df[df['data'].notna()]
    df['ano'] = df['data'].dt.year
    df = df.query('2010 <= ano <= 2025')

    df['tipo_acid'] = df['tipo_acid'].astype(str).str.strip().str.title()
    df['fatais'] = pd.to_numeric(df['fatais'], errors='coerce').fillna(0).astype(int)
    df['acidente_fatal'] = np.where(df['fatais'] > 0, 'Fatal', 'Não Fatal')

    # Hora
    def parse_hora(valor):
        try:
            return parser.parse(str(valor)).time()
        except:
            return np.nan

    if 'hora' in df.columns:
        df['hora'] = df['hora'].astype(str).apply(parse_hora)

    return df


def plot_acidentes_ano(df):
    acidentes_ano = df[df['ano'] < 2025].groupby('ano').size().sort_index()

    dados_2025 = df[df['ano'] == 2025]
    if not dados_2025.empty:
        meses = dados_2025['data'].dt.month.nunique()
        proj_2025 = int(len(dados_2025) / meses * 12)
        acidentes_ano.loc[2025] = proj_2025

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=acidentes_ano.index, y=acidentes_ano.values, palette="Blues_d", ax=ax)
    ax.set_title('Acidentes por Ano (com Projeção 2025)')
    ax.set_ylabel('Número de Acidentes')
    return fig


def plot_top_tipos(df):
    top_tipos = df['tipo_acid'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=top_tipos.values, y=top_tipos.index, palette="OrRd_r", ax=ax)
    ax.set_title("Top 10 Tipos de Acidentes")
    ax.set_xlabel("Ocorrências")
    return fig


def plot_fatais_por_ano(df):
    fatais_ano = df.groupby('ano')['fatais'].sum()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=fatais_ano.index, y=fatais_ano.values, palette="Reds_d", ax=ax)
    ax.set_title("Vítimas Fatais por Ano")
    ax.set_ylabel("Número de Fatais")
    return fig


def plot_distribuicao_horaria(df):
    horas = df['hora'].dropna()
    horas = pd.Series([h.hour for h in horas])
    counts = horas.value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=counts.index, y=counts.values, color='skyblue', ax=ax)
    ax.set_title("Distribuição de Acidentes por Hora do Dia")
    ax.set_xlabel("Hora")
    ax.set_ylabel("Ocorrências")
    return fig


def gerar_mapa(df):
    mapa = folium.Map(location=[-30.1, -51.15], zoom_start=11)
    cluster = MarkerCluster().add_to(mapa)

    for lat, lon in df[['latitude', 'longitude']].dropna().itertuples(index=False):
        folium.Marker([lat, lon]).add_to(cluster)

    return mapa

# === Interface Streamlit ===

st.set_page_config(page_title="Dashboard de Acidentes", layout="wide")
st.title("🚗 Dashboard de Acidentes de Trânsito")

# Carregamento
caminho = "data/cat_acidentes.csv"
df = carregar_dados(caminho)

# Filtros
st.sidebar.header("Filtros")

anos = st.sidebar.multiselect("Ano", sorted(df['ano'].unique()), default=sorted(df['ano'].unique()))
tipos = st.sidebar.multiselect("Tipo de Acidente", sorted(df['tipo_acid'].unique()), default=sorted(df['tipo_acid'].unique()))

# Novo filtro por fatalidade com botão de rádio
filtro_fatal = st.sidebar.radio("Acidentes Fatais?", ["Todos", "Fatal", "Não Fatal"])
if filtro_fatal == "Fatal":
    fatais = ["Fatal"]
elif filtro_fatal == "Não Fatal":
    fatais = ["Não Fatal"]
else:
    fatais = df['acidente_fatal'].unique().tolist()

df_filt = df[
    (df['ano'].isin(anos)) &
    (df['tipo_acid'].isin(tipos)) &
    (df['acidente_fatal'].isin(fatais))
]

# Layout de gráficos
col1, col2 = st.columns(2)

with col1:
    st.pyplot(plot_acidentes_ano(df_filt))

with col2:
    st.pyplot(plot_fatais_por_ano(df_filt))

st.pyplot(plot_top_tipos(df_filt))
st.pyplot(plot_distribuicao_horaria(df_filt))

st.subheader("🗺️ Mapa de Acidentes")
mapa = gerar_mapa(df_filt)
st_folium(mapa, width=1200, height=500)
