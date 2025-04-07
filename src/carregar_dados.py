import pandas as pd
import numpy as np

def carregar_e_tratar_csv(caminho_csv: str) -> pd.DataFrame:
    # Carregamento inicial
    df = pd.read_csv(caminho_csv, sep=';').copy()

    

    # Filtrando coordenadas válidas
    df = df.dropna(subset=['latitude', 'longitude']).copy()
    df[['latitude', 'longitude']] = df[['latitude', 'longitude']].astype(float)
    df = df[
        (df['latitude'] != 0) &
        (df['longitude'] != 0) &
        (df['latitude'].between(-30.30, -29.80)) &
        (df['longitude'].between(-51.40, -50.90))
    ].copy()

    # Convertendo coluna 'data' e criando coluna 'ano'
    df['data'] = pd.to_datetime(df['data'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    df = df[df['data'].notna()].copy()
    df['ano'] = df['data'].dt.year
    df = df.query('2010 <= ano <= 2025').copy()

    # Padronizando tipo de acidente
    df['tipo_acid'] = df['tipo_acid'].astype(str).str.strip().str.title()

    # Tratando coluna fatais e criando categoria fatal/não fatal
    df['fatais'] = pd.to_numeric(df['fatais'], errors='coerce').fillna(0).astype(int)
    df['acidente_fatal'] = np.where(df['fatais'] > 0, 'Fatal', 'Não Fatal')

    # Convertendo coluna 'hora', se existir
    # Convertendo coluna 'hora', se existir
    if 'hora' in df.columns:
        try:
            df['hora'] = pd.to_datetime(df['hora'], format='%H:%M:%S.%f', errors='coerce')
            df['hora'] = df['hora'].dt.time  # pega só o horário, sem data
        except Exception as e:
            print('Erro ao converter hora:', e)


            


    return df





