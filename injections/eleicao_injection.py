import zipfile
import pandas as pd
from schemas.eleicao import eleicao_entity
from config.database import mongodb_client
from pydantic import ValidationError
import sys

# Caminho dos arquivos ZIP e das colunas desejadas
ZIP_PATH_CANDIDATOS = 'resources/consulta_cand_2024.zip'
ZIP_PATH_VAGAS = 'resources/consulta_vagas_2024.zip'

# Colunas para realizar o tratamento
colunas_desejadas_candidatos = [
    "CD_ELEICAO", "DS_ELEICAO", "DT_ELEICAO", "ANO_ELEICAO",
    "CD_TIPO_ELEICAO", "NM_TIPO_ELEICAO", "TP_ABRANGENCIA", "NR_TURNO"
]

# ------------ LEITURA DOS ARQUIVOS DE CANDIDATOS ------------
with zipfile.ZipFile(ZIP_PATH_CANDIDATOS, 'r') as zip_ref_candidatos:
    # Filtrar apenas os arquivos CSV de candidatos
    arquivos_candidatos = [f for f in zip_ref_candidatos.namelist() if f.endswith('.csv')]
    
    dataframes_candidatos = []
    for arquivo_candidato in arquivos_candidatos:
        if "consulta_cand" not in arquivo_candidato:
            print(f"AVISO: O arquivo {arquivo_candidato} não contém 'consulta_cand' no nome.")
            sys.exit(1)  # Interrompe o programa imediatamente

        else:
            with zip_ref_candidatos.open(arquivo_candidato) as csv_file_candidato:
                try:
                    df_candidato = pd.read_csv(csv_file_candidato, sep=';', encoding='latin1', usecols=colunas_desejadas_candidatos)
                    dataframes_candidatos.append(df_candidato)
                except ValueError as e:
                    print(f"Erro ao ler o arquivo {arquivo_candidato}: {str(e)}")
                    sys.exit(1)  # Interrompe o programa imediatamente

# Remover duplicatas com base no código da eleição
df_candidatos_unico = df_candidato.drop_duplicates(subset=['CD_ELEICAO'])

# ------------ LEITURA DOS ARQUIVOS DE VAGAS ------------
# Função para ler todos os arquivos CSV de um ZIP e juntar em um único DataFrame
with zipfile.ZipFile(ZIP_PATH_VAGAS, 'r') as zip_ref:  # Abrindo diretamente o arquivo ZIP
    # Filtra apenas os arquivos CSV de vagas
    arquivos_vagas = [f for f in zip_ref.namelist() if f.endswith('.csv')]
    
    data_frame_vagas = []
    for arquivo_vaga in arquivos_vagas:
        if "consulta_vagas" not in arquivo_vaga:
            print(f"AVISO: O arquivo {arquivo_vaga} não contém 'consulta_vagas' no nome.")
            sys.exit(1)  # Interrompe o programa imediatamente
        else:
            with zip_ref.open(arquivo_vaga) as file:
                try:
                    df_vagas = pd.read_csv(file, sep=';', encoding='latin1', usecols=['CD_ELEICAO', 'QT_VAGA'])
                    data_frame_vagas.append(df_vagas)
                except ValueError as e:
                    print(f"Erro ao ler o arquivo {arquivo_vaga}: {str(e)}")
                    sys.exit(1)  # Interrompe o programa imediatamente

# Somar os valores de 'QT_VAGA' para cada 'CD_ELEICAO'
df_vagas_sum = df_vagas.groupby('CD_ELEICAO')['QT_VAGA'].sum().reset_index()

# Agora, unir os dados de vagas com a soma dos valores de 'QT_VAGA' para cada código de eleição
df_final = pd.merge(df_candidatos_unico, df_vagas_sum, on='CD_ELEICAO', how='left')

# # Preencher valores ausentes (NaN) com 0
df_final['QT_VAGA'] = df_final['QT_VAGA'].fillna(0)
df_final['QT_VAGA'] = df_final['QT_VAGA'].astype(int)


print("Tratamento dos dados finalizados.")
print(f"Total de dados a serem carregados: {df_final.shape[0]}")
print("Inserindo dados no banco. Aguarde...")

# ------------ INÍCIO DA INSERÇÃO NO BANCO DE DADOS ------------
db = mongodb_client['eleicoes']  # Nome do banco de dados
collection = db['eleicoes']  # Nome da coleção onde os dados serão inseridos

for eleicao in df_final.to_dict(orient="records"):
    try:
        # Criar a instância de EleicaoBase
        dados_eleicao = eleicao_entity(eleicao)

        # Converte os dados para dicionário
        dados_dict = dados_eleicao.model_dump()

        # Substituir o campo '_id' pelo valor de 'cd_eleicao' como o identificador
        dados_dict['_id'] = dados_dict['cd_eleicao']

        # Verificar se já existe o cd_eleicao no banco de dados
        if collection.find_one({'cd_eleicao': dados_eleicao.cd_eleicao}) is not None:
            print(f"Eleição com cd_eleicao {dados_eleicao.cd_eleicao} já existe no banco de dados.")
        else:
            # Inserir no banco de dados
            result = collection.insert_one(dados_dict)  # Inserindo o dicionário com o campo '_id' alterado

            # Verificar se o documento foi inserido corretamente
            if result.inserted_id:
                print(f"Eleição com cd_eleicao {dados_eleicao.cd_eleicao} inserida com sucesso!")
            else:
                print("Erro ao inserir os dados no banco.")

    except ValidationError as e:
        print(f"Erro de validação: {e}")
    except Exception as e:
        print(f"Algo deu errado: {e}")
