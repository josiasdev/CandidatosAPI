import zipfile
import pandas as pd
from schemas.accident import accident_entity
from config.database import mongodb_client

ZIP_PATH = 'resources/Acidentes_DadosAbertos_20230912.csv.zip'
CSV_FILENAME = 'Acidentes_DadosAbertos_20230912.csv'

data_array = []

with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
    with zip_ref.open(CSV_FILENAME) as csv_file:
        accidents = pd.read_csv(csv_file, sep=';')
        accidents = accidents[accidents['tp_curva'] != 'NAO INFORMADO']
        accidents = accidents[accidents['tp_curva'] != 'DESCONHECIDO']
        accidents = accidents[accidents['cond_meteorologica'] != 'NAO INFORMADO']
        accidents = accidents[~accidents['bairro_acidente'].isnull()]
    
    
    db = mongodb_client['trafficAccidents']
    collection = db['accident']
    for accident in accidents.to_dict(orient="records"):
        try:
            accident_data = accident_entity(accident)
            if(collection.find_one({'num_acidente': accident_data['num_acidente']}) is not None):
                print('Accident already exists')
            else:
                result = collection.insert_one(accident_data)
                
                if (created := collection.find_one({"_id": result.inserted_id})) is None:
                    print('Something went wrong and the data was not inserted')
            print('Operation finshed with success!')
        except Exception as e:
            print("Something went wrong", e)