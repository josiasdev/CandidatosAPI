import zipfile
import pandas as pd
from schemas.victim import victim_entity
from config.database import mongodb_client


ZIP_PATH = 'resources/Vitimas_DadosAbertos_20230912.csv.zip'
CSV_FILENAME = 'transa.csv'

data_array = []


#Colunas a serem limpas
#Remover dados com os valores 'DESCONHECIDO' e 'NÃO INFORMADO'
#Limpeza necessária pois é preciso que os dados sejam íntegros
columns_to_clean = [
    'num_acidente', 'chv_localidade', 'data_acidente', 'uf_acidente',
    'ano_acidente', 'mes_acidente', 'genero', 'faixa_idade', 'gravidade_lesao', 'equip_seguranca',
    'tp_envolvido'
]

with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
    with zip_ref.open(CSV_FILENAME) as csv_file:
        victims = pd.read_csv(csv_file, sep=';')

        # Remover linhas que contenham "NAO INFORMADO" ou "DESCONHECIDO" nas colunas selecionadas
        for column in columns_to_clean:
            victims = victims[(victims[column] != "NAO INFORMADO") & (victims[column] != "DESCONHECIDO")]
        
        # Remover duplicados a partir do num_acidente (pegar o primeiro resultado)
        victims = victims.drop_duplicates(subset=['num_acidente'], keep='first')  

        # Contar quantas linhas foram removidas
        final_result = victims.shape[0]
        print(f"Total after clean up: {final_result}")
        
    db = mongodb_client['trafficAccidents']
    collection = db['victim']
    for victim in victims.to_dict(orient="records"):
        try:
            victim_data = victim_entity(victim)
            if(collection.find_one({'num_acidente': victim_data['num_acidente']}) is not None):
                print('Accident already exists')
            else:
                result = collection.insert_one(victim_data)
                
                if (created := collection.find_one({"_id": result.inserted_id})) is None:
                    print('Something went wrong and the data was not inserted')
            print('Operation finshed with success!')
        except Exception as e:
            print("Something went wrong", e)