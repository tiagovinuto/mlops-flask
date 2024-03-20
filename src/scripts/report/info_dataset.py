import pandas as pd
from IPython.display import display
import os

def read_dataset(path, file):
    try:
        if file.endswith('.csv'):
            nome_df = pd.read_csv(path+file)
        elif file.endswith('.json'):
            nome_df = pd.read_json(path+file)
        elif file.endswith('.xlsx'):
            nome_df = pd.read_excel(path+file, header= 1)
    except FileNotFoundError as e:
        print(f'O arquivo {file} não foi encontrado no diretório {path}.')
        nome_df = None
    return nome_df

def list_dataset(path):
    files_len = len(os.listdir(path))
    
    if files_len > 0:
        file_names = os.listdir(path)
        print(f"Existem {files_len} arquivos contidos no diretorio: {path}")
        return file_names
    else:
        print(f"Não existem arquivos contidos no diretorio: {path}")

def infos_dataset(df):
    print("*"*35+"INFORMAÇÕES GERAIS SOBRE O CONJUNTO DE DADOS"+"*"*35)
    print("\n")
    print("5 primeiros registros do conjunto de dados")
    display(df.head())
    print("5 últimos registros do conjunto de dados")
    display(df.tail())
    print(f"O conjunto de dados possuí: {df.shape[0]} linha e : {df.shape[1]} colunas.")
    print("*"*70)
    
    cat_var = len(df.select_dtypes(include=['object', 'category']).nunique())
    print(f"Quantidade de colunas categoricas: {cat_var}")
    print("*"*70)
    
    colunas_categoricas = df.select_dtypes(include=['object', 'category']).columns.tolist()
    print(f"As colunas categoricas são: {colunas_categoricas}")
    print("*"*70)
    
    num_var = len(df.select_dtypes(include=['number']).nunique())
    print(f"As colunas numéricas são: {num_var}")
    print("*"*70)
    
    colunas_numericas = df.select_dtypes(include=['number']).columns.tolist()
    print(f"As colunas numéricas são: {colunas_numericas}")
    print("*"*70)
    
    nulos = df.isna().sum().sum()
    if nulos > 0: 
        print(f"A quantidade de valores nulos no conjunto de dados são: {nulos}")
        print("*"*70)
        
        print(f"A quantidade de valores nulos no conjunto de dados por colunas:")
        print(df.isna().sum().to_string(dtype=False))
    
    print(f"A quantidade de valores nulos no conjunto de dados são: {df.isna().sum().sum()}")
    
    duplicados = df[df.duplicated()]

    if len(df[df.duplicated()]) > 0:
        print("*"*70)
        print(f"A quantidade de linhas duplicadas é: {len(df[df.duplicated()])}")
        print(duplicados)
    else:
        print("*"*70)
        print(f"O conjunto de dados não possuí duplicados")
        
def read_transform(path, separador=None):
    df = pd.read_csv(path, sep=separador)
    columns = df.columns
    df = df[columns].dropna(how='any')
    return df

def combina_multiplos_csvs(path):
    file_names = [file for file in os.listdir(path) if file.endswith('.csv')]
    dfs = [read_transform(os.path.join(path, i), separador=';') for i in file_names]
    
    df_full = pd.concat(dfs, axis=1)
    df_full.to_csv(f"{path}csvs_combinados.csv", sep=';', index=False)