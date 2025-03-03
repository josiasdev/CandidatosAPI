import zipfile
import pandas as pd
from schemas.locality import locality_entity
from config.database import mongodb_client

ZIP_PATH = 'resources/Acidentes_DadosAbertos_20230912.csv.zip'
CSV_FILENAME = 'Localidade_DadosAbertos_20230912.csv'

data_array = []

with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
    with zip_ref.open(CSV_FILENAME) as csv_file:
        locality_df = pd.read_csv(csv_file, sep=';')
        locality_df = locality_df[locality_df['municipio'] != 'NAO INFORMADO']
        locality_df = locality_df[~locality_df['codigo_ibge'].isnull()]
        locality_df = locality_df[~locality_df['qtde_habitantes'].isnull()]              
    
    db = mongodb_client['trafficAccidents']
    locality_collection = db['locality']
    accidents_collection = db['accident']

    for locality in locality_df.to_dict(orient="records"):
        try:
            chv_localidade = locality.get("chv_localidade")
            
            if not chv_localidade:
                print(f"Chave 'chv_localidade' não encontrada em {locality}")
                continue

            # Busca os acidentes relacionados
            related_accidents = list(accidents_collection.find({"chv_localidade": chv_localidade}))

            # Cria o objeto LocalityBase
            locality_data = locality_entity(locality, related_accidents)

            # Verifica se a localidade já existe
            existing_locality = locality_collection.find_one({'chv_localidade': locality_data.chv_localidade})
            if existing_locality:
                print(f'Locality {locality_data.chv_localidade} already exists')
                locality_id = existing_locality['_id']
            else:
                # Insere a localidade
                result = locality_collection.insert_one(locality_data.dict())
                locality_id = result.inserted_id
                
                if locality_collection.find_one({"_id": locality_id}) is None:
                    print('Something went wrong and the data was not inserted')

            # Atualiza os documentos de acidentes relacionados
            update_result = accidents_collection.update_many(
                {'chv_localidade': locality_data.chv_localidade},
                {'$set': {'locality_id': locality_id}}
            )

            print(f'Updated {update_result.modified_count} accident(s) with locality {locality_data.chv_localidade}')
            print('Operation finished with success!')

        except Exception as e:
            print("Something went wrong:", e)
