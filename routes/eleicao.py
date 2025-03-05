from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
import zipfile
import pandas as pd
from io import BytesIO

# Definindo o roteador
router = APIRouter()

colunas_desejadas_candidatos = [
    "CD_ELEICAO", "DS_ELEICAO", "DT_ELEICAO", "ANO_ELEICAO", 
    "CD_TIPO_ELEICAO", "NM_TIPO_ELEICAO", "TP_ABRANGENCIA", "NR_TURNO"
]

@router.post("/upload/carregar-dados-eleicao")
async def upload_dados_eleicao(
    candidatos_file: UploadFile = File(...),  # Primeiro arquivo de vagas
    vagas_file: UploadFile = File(...),  # Segundo arquivo de candidatos
):
    if not vagas_file or not candidatos_file:
        raise HTTPException(status_code=400, detail="Ambos os arquivos (vagas e candidatos) precisam ser enviados.")

    try:
        # Carregar o arquivo ZIP de Candidatos
        dados_zip_candidatos = await candidatos_file.read()
        with zipfile.ZipFile(BytesIO(dados_zip_candidatos), 'r') as zip_ref_candidatos:
            # Filtrar apenas os arquivos CSV de candidatos
            arquivos_candidatos = [f for f in zip_ref_candidatos.namelist() if f.endswith('.csv')]
            
            dataframes_candidatos = []
            for arquivo_candidato in arquivos_candidatos:
                if "consulta_cand" not in arquivo_candidato:
                    raise HTTPException(status_code=400, detail=f"O arquivo CSV {arquivo_candidato} não contém 'consulta_cand' no nome. Verifique o conteúdo e tente novamente.")
                with zip_ref_candidatos.open(arquivo_candidato) as csv_file_candidato:
                    try:
                        df_candidato = pd.read_csv(csv_file_candidato, sep=';', encoding='latin1', usecols=colunas_desejadas_candidatos)
                        dataframes_candidatos.append(df_candidato)
                    except ValueError as e:
                        raise HTTPException(status_code=400, detail=f"Erro ao ler o arquivo CSV de candidatos: {str(e)}")
            
            # Concatenar todos os DataFrames de candidatos
            df_candidatos = pd.concat(dataframes_candidatos, ignore_index=True)

        # Remover duplicatas com base no código da eleição
        df_candidatos_unico = df_candidatos.drop_duplicates(subset=['CD_ELEICAO'])

        # Carregar o arquivo ZIP de Vagas
        dados_zip_vagas = await vagas_file.read()
        with zipfile.ZipFile(BytesIO(dados_zip_vagas), 'r') as zip_ref_vagas:
            # Filtrar apenas os arquivos CSV de vagas
            arquivos_vagas = [f for f in zip_ref_vagas.namelist() if f.endswith('.csv')]
            
            dataframes_vagas = []
            for arquivo_vaga in arquivos_vagas:
                if "consulta_vagas" not in arquivo_vaga:
                    raise HTTPException(status_code=400, detail=f"O arquivo CSV {arquivo_vaga} não contém 'consulta_vagas' no nome. Verifique o conteúdo e tente novamente.")
                with zip_ref_vagas.open(arquivo_vaga) as csv_file_vaga:
                    try:
                        df_vaga = pd.read_csv(csv_file_vaga, sep=';', encoding='latin1', usecols=['CD_ELEICAO', 'QT_VAGA'])
                        dataframes_vagas.append(df_vaga)
                    except ValueError as e:
                        raise HTTPException(status_code=400, detail=f"Erro ao ler o arquivo CSV de vagas: {str(e)}")
            
            # Concatenar todos os DataFrames de vagas
            df_vagas = pd.concat(dataframes_vagas, ignore_index=True)

        # Somar os valores de 'QT_VAGA' para cada 'CD_ELEICAO'
        df_vagas_sum = df_vagas.groupby('CD_ELEICAO')['QT_VAGA'].sum().reset_index()

        # Agora, unir os dados de vagas com a soma dos valores de 'QT_VAGA' para cada código de eleição
        df_final = pd.merge(df_candidatos_unico, df_vagas_sum, on='CD_ELEICAO', how='left')

        # Preencher valores ausentes (NaN) com 0
        df_final['QT_VAGA'] = df_final['QT_VAGA'].fillna(0)
        df_final['QT_VAGA'] = df_final['QT_VAGA'].astype(int)

        # Retornar o resultado final como JSON
        return JSONResponse(content=df_final.to_dict(orient="records"))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
