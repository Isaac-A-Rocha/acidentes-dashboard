import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
import pandas as pd
from dateutil import parser

# Função para tratamento da hora
def parse_hora(valor):
    try:
        return parser.parse(str(valor)).time()
    except:
        return np.nan

def plot_acidentes_ano(df):
    sns.set_style("whitegrid")
    sns.set_context("talk")

    acidentes_ano = df[df['ano'] < 2025].groupby('ano').size().sort_index()

    dados_2025 = df[df['ano'] == 2025]
    if not dados_2025.empty:
        meses = dados_2025['data'].dt.month.nunique()
        proj_2025 = int(len(dados_2025) / meses * 12)
        acidentes_ano.loc[2025] = proj_2025

    fig, ax = plt.subplots(figsize=(14, 8))
    bars = ax.bar(acidentes_ano.index.astype(str), acidentes_ano.values,
                  color=sns.color_palette('Blues_d', len(acidentes_ano)))
    ax.set_title('Acidentes por Ano (com Projeção 2025)')
    ax.set_xlabel('Ano')
    ax.set_ylabel('Número de Acidentes')
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 10, f'{int(h)}', ha='center')
    plt.tight_layout()
    os.makedirs("visualizations", exist_ok=True)
    plt.savefig("visualizations/plot_acidentes_ano.png")
    plt.close()

def plot_top_tipos(df):
    top_tipos = df['tipo_acid'].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(12, 10))
    bars = ax.barh(top_tipos.index, top_tipos.values,
                   color=sns.color_palette('OrRd_r', len(top_tipos)))
    ax.set_title('Top 10 Tipos de Acidentes')
    ax.set_xlabel('Ocorrências')
    ax.invert_yaxis()
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 10, bar.get_y() + bar.get_height() / 2, f'{int(w)}', va='center')
    plt.tight_layout()
    os.makedirs("visualizations", exist_ok=True)
    plt.savefig("visualizations/plot_top_tipos.png")
    plt.close()

def plot_fatais_por_ano(df):
    fatais_ano = df.groupby('ano')['fatais'].sum()

    fig, ax = plt.subplots(figsize=(14, 8))
    bars = ax.bar(fatais_ano.index.astype(str), fatais_ano.values,
                  color=sns.color_palette('Reds_d', len(fatais_ano)))
    ax.set_title('Total de Vítimas Fatais por Ano')
    ax.set_xlabel('Ano')
    ax.set_ylabel('Número de Vítimas Fatais')
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 1, f'{int(h)}', ha='center')
    plt.tight_layout()
    plt.savefig("visualizations/plot_fatais_por_ano.png")
    plt.close()

def plot_distribuicao_acidentes(df):
    if 'hora' in df.columns:
        df['hora'] = df['hora'].astype(str).apply(parse_hora)

    fig, ax = plt.subplots(figsize=(12, 8))

    horas = df['hora'].dropna()
    horas = pd.Series([h.hour for h in horas])
    counts = horas.value_counts().sort_index()

    bars = ax.bar(counts.index, counts.values, color='skyblue')

    ax.set_title('Distribuição de Acidentes por Hora do Dia')
    ax.set_xlabel('Hora do Dia')
    ax.set_ylabel('Quantidade de Acidentes')
    ax.set_xticks(range(0, 24))

    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 2, f'{int(h)}', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig("visualizations/plot_distribuicao_hora.png")
    plt.close()

def plot_acidentes_por_tipo_fatal(df):
    tipo_fatal = df.groupby(['tipo_acid', 'acidente_fatal']).size().unstack().fillna(0)
    tipo_fatal = tipo_fatal.sort_values('Fatal', ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(14, 8))
    tipo_fatal.plot(kind='bar', stacked=True, ax=ax,
                    color=['#4daf4a', '#e41a1c'])
    ax.set_title('Top 10 Tipos de Acidentes - Fatais vs Não Fatais')
    ax.set_xlabel('Tipo de Acidente')
    ax.set_ylabel('Número de Acidentes')
    plt.tight_layout()
    plt.savefig("visualizations/plot_fatal_vs_nao_fatal.png")
    plt.close()
