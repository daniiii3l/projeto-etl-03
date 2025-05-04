import os
import pandas as pd
import yfinance as yf
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Carregar variaveis de ambiente
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_SCHEMA = os.getenv('DB_SCHEMA')

# Criando conexao com o banco
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"
engine = create_engine(DATABASE_URL)


# Definindo quais ativos iremos realizar busca
# 'CL=F' = petroleo / 'GC=F' = ouro / 'SI=F' = prata
commodities = ['CL=F', 'GC=F', 'SI=F']

# Função que irá realizar a busca do commoditie e retornar um dataframe
def buscar_dados_commodities(simbolo, periodo='5d', intervalo='1d'):
    ticker = yf.Ticker(simbolo)
    dados = ticker.history(period=periodo, interval=intervalo)[['Close']]
    dados['simbolo'] = simbolo
    return dados

# Função que irá consolidar todos os commodities
def buscar_todos_commodities(commodities):
    todos_dados = []
    for simbolo in commodities:
        dados = buscar_dados_commodities(simbolo)
        todos_dados.append(dados)
    return pd.concat(todos_dados)

def salvar_dados_postegres(df):
    df.to_sql('commodities', engine, if_exists='replace', index=True, index_label='Date', schema='public')


if __name__ == '__main__':
    dados_concatenados = buscar_todos_commodities(commodities)
    salvar_dados_postegres(dados_concatenados)