import re
import zipfile
import pandas as pd
from schemas.candidato import candidato_entity
from config.database import mongodb_client
from models.candidato import CandidatoCreate

ZIP_PATH = 'resources/consulta_cand_2024.zip'
CSV_PATTERN = re.compile(r'^.*\d{4}_(BRASIL|[A-Z]{2})\.csv$')

with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
    total_candidatos = 0
    for file_name in zip_ref.namelist():
        if file_name.startswith("__MACOSX/"):  # Skip macOS metadata files
            continue
        if not CSV_PATTERN.match(file_name):  # prevent OS files to be processed
            print(f"Skipping file: {file_name}")
            continue
        if file_name.endswith('.csv'):
            print(f"Processing file: {file_name}")

            with zip_ref.open(file_name) as csv_file:
                candidatos = pd.read_csv(csv_file, encoding='latin1', sep=';')
                candidatos.columns = candidatos.columns.str.lower()

                candidatos["dt_nascimento"] = pd.to_datetime(
                    candidatos["dt_nascimento"], format="%d/%m/%Y", errors="coerce"
                )
                
                for key in CandidatoCreate.model_fields.keys():
                    candidatos = candidatos[~candidatos[key].isnull()]
    

            total_candidatos += len(candidatos)
            # db = mongodb_client['eleicoes']
            # collection = db['candidato']
            # for candidato in candidatos.to_dict(orient="records"):
            #     try:
            #         candidato_data = candidato_entity(candidato)
            #         if(collection.find_one({'nr_titulo_eleitoral_candidato': candidato_data['nr_titulo_eleitoral_candidato']}) is not None):
            #             print('Candidato already exists')
            #         else:
            #             result = collection.insert_one(candidato_data)
                        
            #             if (created := collection.find_one({"_id": result.inserted_id})) is None:
            #                 print('Something went wrong and the data was not inserted')
            #         print('Operation finshed with success!')
            #     except Exception as e:
            #         print("Something went wrong", e)
    print(total_candidatos)