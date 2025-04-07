from src.carregar_dados import carregar_e_tratar_csv
from src.graficos import plot_acidentes_ano, plot_top_tipos, plot_acidentes_por_tipo_fatal,plot_distribuicao_acidentes,plot_fatais_por_ano
from src.mapa import gerar_mapa

def main():
    df = carregar_e_tratar_csv('data/cat_acidentes.csv')

    print("\n=== Amostra da coluna 'hora' ===")
    print(df['hora'].head(10))

    print("\n=== Tipos únicos detectados na coluna 'hora' ===")
    print(df['hora'].apply(lambda x: type(x)).value_counts())


    plot_acidentes_ano(df)
    plot_top_tipos(df)
    plot_fatais_por_ano(df)
    plot_acidentes_por_tipo_fatal(df)
    plot_distribuicao_acidentes(df)
    

    gerar_mapa(df)

if __name__ == "__main__":
    main()