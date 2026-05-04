from random import randint
import boto3
from dotenv import load_dotenv
import pandas as pd
import datetime
import re

from utils import get_bucket_content, get_buckets, get_max_date, get_s3

load_dotenv()

def get_lastest_folder_date():
    s3 = get_s3()
    folders = get_bucket_content(s3, 'raw-sacramento', 'folder')
    last_date = get_max_date(folders)
    return last_date

    

def create_cliente():
    # IDCliente	Cliente	Estado	Sexo	Status
    # ler tabela clientes, pega ultimo idcliente e gerar aleatoriamento os outros dados
    # Padrão -> simular dados de um ERP -> São registrados novos produtos, clientes e etc todo dia
    # Dessa forma, do ERP eu vou pegar a tabela inteira, visualizar o que mudou, e acrescentar na silver - dimensoes
    # Ler o raw, ler a silver, ver o que tem de diferença e acrescenta

    params = {
        'ingestion_date': datetime.date.today().strftime('%d_%m_%Y'),
    }

    last_date = get_lastest_folder_date()

    last_clientes = pd.read_csv(f's3://raw-sacramento/clientes-produtos/{params['ingestion_date']}')




# def create_produto():
# def create_vendas():
# def create_vendedor():
# def create_itensvenda():