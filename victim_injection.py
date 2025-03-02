import zipfile
import pandas as pd
from schemas.victim import victim_entity
from config.database import mongodb_client


ZIP_PATH = 'resources/Vitimas_DadosAbertos_20230912.csv.zip'
CSV_FILENAME = 'Vitimas_DadosAbertos_20230912.csv'

data_array = []

#Colunas a serem limpas
#Remover dados com os valores 'DESCONHECIDO' e 'NÃO INFORMADO'
#Limpeza necessária pois é preciso que os dados sejam íntegros
columns_to_clean = [
    'num_acidente', 'chv_localidade', 'data_acidente', 'uf_acidente',
    'ano_acidente', 'mes_acidente', 'mes_ano_acidente', 'faixa_idade',
    'genero', 'tp_envolvido', 'qtde_envolvidos', 'qtde_feridosilesos', 'ind_motorista', 'susp_alcool', 'gravidade_lesao',
    'qtde_obitos'
]

with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
    with zip_ref.open(CSV_FILENAME) as csv_file:
        victims = pd.read_csv(csv_file, sep=';')

        # Remover linhas que contenham "NAO INFORMADO" ou "DESCONHECIDO" nas colunas selecionadas
        for column in columns_to_clean:
            victims = victims[(victims[column] != "NAO INFORMADO") & (victims[column] != "DESCONHECIDO")]

        # Na coluna quantidade de envolvidos, o retorno deve ser somente aqueles diferente de 0
        victims = victims[victims['qtde_envolvidos'] != 0]

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