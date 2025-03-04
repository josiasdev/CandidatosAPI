import zipfile
import pandas as pd

# Caminho dos arquivos ZIP e dos CSV
ZIP_PATH_CANDIDATOS = '/content/consulta_cand_2024.zip'
CSV_FILENAME_CANDIDATOS = 'consulta_cand_2024_CE.csv'

ZIP_PATH_VAGAS = '/content/consulta_vagas_2024.zip'
CSV_FILENAME_VAGAS = 'consulta_vagas_2024_CE.csv'

# Colunas desejadas para vagas
colunas_desejadas_vagas = [
    "CD_ELEICAO", "DS_ELEICAO", "DT_ELEICAO", "ANO_ELEICAO",
    "CD_TIPO_ELEICAO", "NM_TIPO_ELEICAO", "DT_POSSE"
]

# Processar o ZIP de Vagas
with zipfile.ZipFile(ZIP_PATH_VAGAS, 'r') as zip_ref:
    with zip_ref.open(CSV_FILENAME_VAGAS) as csv_file:
        # Ler o CSV com as colunas desejadas de vagas
        vagas = pd.read_csv(csv_file, sep=';', encoding='latin1', usecols=colunas_desejadas_vagas)

# Garantir que os códigos de eleição e as datas de posse sejam únicas
vagas_unicas = vagas.drop_duplicates(subset=['CD_ELEICAO', 'DT_POSSE'])

# Carregar o CSV dos candidatos
with zipfile.ZipFile(ZIP_PATH_CANDIDATOS, 'r') as zip_ref:
    with zip_ref.open(CSV_FILENAME_CANDIDATOS) as csv_file:
        # Ler o CSV com os dados dos candidatos
        candidatos = pd.read_csv(csv_file, sep=';', encoding='latin1')

# Filtrar os candidatos com os códigos de eleição presentes em vagas_unicas
candidatos_filtrados = candidatos[candidatos['CD_ELEICAO'].isin(vagas_unicas['CD_ELEICAO'])]

# Merge entre as tabelas
resultado = pd.merge(vagas_unicas, candidatos_filtrados[['CD_ELEICAO', 'TP_ABRANGENCIA', 'NR_TURNO']], 
                     on='CD_ELEICAO', how='left')

resultado = resultado.drop_duplicates(subset=['CD_ELEICAO', 'DT_POSSE'])


# Obter os IDs que estão em 'candidatos' mas não estão em 'resultado'
ids_nao_encontrados = candidatos[~candidatos['CD_ELEICAO'].isin(resultado['CD_ELEICAO'])]

# Garantir que cada 'CD_ELEICAO' seja único
ids_nao_encontrados_unicos = ids_nao_encontrados.drop_duplicates(subset=['CD_ELEICAO'])

# Selecionar apenas as colunas desejadas e adicionar 'DT_POSSE' com valor fixo
ids_nao_encontrados_unicos = ids_nao_encontrados_unicos[
    ['CD_ELEICAO', 'DS_ELEICAO', 'DT_ELEICAO', 'ANO_ELEICAO', 
     'CD_TIPO_ELEICAO', 'NM_TIPO_ELEICAO', 'TP_ABRANGENCIA', 'NR_TURNO']
].copy()

# Adicionar a coluna 'DT_POSSE' com o valor "00/00/0000"
ids_nao_encontrados_unicos['DT_POSSE'] = "00/00/0000"

# Conteúdo de eleição já tratado
resultado_final = pd.concat([resultado, ids_nao_encontrados_unicos])