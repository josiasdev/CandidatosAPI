import zipfile
import pandas as pd
from schemas.highway import highway_entity
from config.database import mongodb_client

ZIP_PATH = 'resources/Acidentes_DadosAbertos_20230912.csv.zip'
CSV_FILENAME = 'Acidentes_DadosAbertos_20230912.csv'

data_array = []

with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
    with zip_ref.open(CSV_FILENAME) as csv_file:
        highway = pd.read_csv(csv_file, sep=';')
        highway = highway[highway['tp_rodovia'] != 'NAO INFORMADO']
        highway = highway[highway['tp_rodovia'] != 'DESCONHECIDO']
        highway = highway[highway['cond_pista'] != 'DESCONHECIDO']
        highway = highway[highway['tp_cruzamento'] != 'DESCONHECIDO']
        highway = highway[highway['tp_cruzamento'] != 'NAO INFORMADO']
        highway = highway[highway['tp_pavimento'] != 'DESCONHECIDO']
        highway = highway[highway['tp_pavimento'] != 'NAO INFORMADO']
        highway = highway[highway['tp_curva'] != 'DESCONHECIDO']
        highway = highway[highway['tp_curva'] != 'NAO INFORMADO']
        highway = highway[highway['lim_velocidade'] != 'NAO INFORMADO']
        highway = highway[highway['ind_guardrail'] != 'NAO INFORMADO']    
    
    db = mongodb_client['trafficAccidents']
    collection = db['highway']
    for highway in highway.to_dict(orient="records"):
        try:
            highway_data = highway_entity(highway)
            if(collection.find_one({'num_acidente': highway_data['num_acidente']}) is not None):
                print('Highway already exists')
            else:
                result = collection.insert_one(highway_data)
                
                if (created := collection.find_one({"_id": result.inserted_id})) is None:
                    print('Something went wrong and the data was not inserted')
            print('Operation finshed with success!')
        except Exception as e:
            print("Something went wrong", e)