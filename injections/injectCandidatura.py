import sys
import zipfile
import pandas as pd
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent)) # Adicione o diretório raiz do projeto ao sys.path
from schemas.Candidatura import candidatura_entity
from config.database import mongodb_client

# Caminhos dos arquivos
ZIP_PATH_CANDIDATO = '/Users/robso/Downloads/dataset/consulta_cand_2024.zip'
CSV_FILENAME_CANDIDATO = 'consulta_cand_2024_BRASIL.csv'

ZIP_PATH_CASSACAO = '/Users/robso/Downloads/dataset/motivo_cassacao_2024.zip'
CSV_FILENAME_CASSACAO = 'motivo_cassacao_2024_BRASIL.csv'

data_array = []

# Carregar dados de candidatura
with zipfile.ZipFile(ZIP_PATH_CANDIDATO, 'r') as zip_ref:
    with zip_ref.open(CSV_FILENAME_CANDIDATO) as csv_file:
        candidatura_df = pd.read_csv(csv_file, sep=';', encoding='cp1252')
        candidatura_df = candidatura_df[['SQ_CANDIDATO','NM_CANDIDATO', 'CD_ELEICAO', 'SG_UF', 'DS_CARGO', 'NR_CANDIDATO',
                                         'NR_PARTIDO', 'SG_PARTIDO', 'NM_PARTIDO', 'NR_TURNO', 'TP_AGREMIACAO',
                                         'DS_SIT_TOT_TURNO']]

# Carregar dados de cassação
with zipfile.ZipFile(ZIP_PATH_CASSACAO, 'r') as zip_ref:
    with zip_ref.open(CSV_FILENAME_CASSACAO) as csv_file:
        cassacao_df = pd.read_csv(csv_file, sep=';', encoding='cp1252')
        cassacao_df = cassacao_df[['SQ_CANDIDATO', 'DS_TP_MOTIVO', 'DS_MOTIVO']]


# Mesclar os DataFrames com base na chave comum 'SQ_CANDIDATO'
merged_df = pd.merge(candidatura_df, cassacao_df, on='SQ_CANDIDATO', how='left')

print(merged_df.head())
print('\n\n')
print(merged_df.dtypes)
print('\n\n')
print(merged_df.count())
print('\n\n')
print(merged_df.isnull().sum())

# Conectar ao banco MongoDB
db = mongodb_client['Candidatos']
collection = db['candidatura']

for _, row in merged_df.iterrows():
    entity = candidatura_entity(row.to_dict())
    collection.insert_one(entity)

print("Dados inseridos com sucesso!")