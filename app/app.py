import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Carregar variaveis de ambiente
load_dotenv()

# Variaveis de amiente para conexão com o banco
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_SCHEMA = os.getenv('DB_SCHEMA')

# String de conexão com o banco
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"
engine = create_engine(DATABASE_URL)

# Funcao para retorno da Query SQL
def get_data():
   query = """
   SELECT 
      *
   FROM 
      public.dm_commodities
   """
   df = pd.read_sql(query, engine)
   return df

# Configurar pag do streamlit
st.set_page_config(page_title="Dashboard de Commodities", layout="wide")

# Definir titulo e descricao
st.title="Dashboard de Commodities"

st.write("Esse é um Dashboard que mostra os dados de commodities e suas transações.")

df = get_data()

# Plotar dataframe dentro do streamlit
st.dataframe(df)