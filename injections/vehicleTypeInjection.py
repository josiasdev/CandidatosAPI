import zipfile
import pandas as pd
from schemas.vehicleType import vehicle_entity
from config.database import mongodb_client

ZIP_PATH_TYPE_VEHICLE = '/home/rafael/Estudos/UFC/Persistencia/TipoVeiculo_DadosAbertos_20230912.csv.zip'
CSV_FILENAME_TYPE_VEHICLE = 'TipoVeiculo_DadosAbertos_20230912.csv'

ZIP_PATH_ACCIDENT = '/home/rafael/Estudos/UFC/Persistencia/Acidentes_DadosAbertos_20230912.csv.zip'
CSV_FILENAME_ACCIDENT = 'Acidentes_DadosAbertos_20230912.csv'

ZIP_PATH_LOCALITY = '/home/rafael/Estudos/UFC/Persistencia/Localidade_DadosAbertos_20230912.csv.zip'
CSV_FILENAME_LOCALITY = 'Localidade_DadosAbertos_20230912.csv'

data_array = []

with zipfile.ZipFile(ZIP_PATH_TYPE_VEHICLE, 'r') as zip_ref:
    with zip_ref.open(CSV_FILENAME_TYPE_VEHICLE) as csv_file:
        vehicles = pd.read_csv(csv_file, sep=';')
        vehicles = vehicles[vehicles['ind_veic_estrangeiro'] != 'NAO INFORMADO']
        vehicles = vehicles[vehicles['ind_veic_estrangeiro'] != 'DESCONHECIDO']
        vehicles = vehicles[vehicles['tipo_veiculo'] != 'NAO INFORMADO']
        vehicles = vehicles[vehicles['tipo_veiculo'] != 'DESCONHECIDO']
        vehicles = vehicles.head(76334)
        print(vehicles.count())

with zipfile.ZipFile(ZIP_PATH_ACCIDENT, 'r') as zip_ref_accident:
    with zip_ref_accident.open(CSV_FILENAME_ACCIDENT) as csv_file_accident:
        accidents = pd.read_csv(csv_file_accident, sep=';', dtype={'num_acidente': str}, low_memory=False)
        # Process accidents data as needed
        accidents = accidents[['num_acidente', 'lim_velocidade', 'tp_pista']]
        accidents = accidents[accidents['lim_velocidade'] != 'NAO INFORMADO']
        accidents = accidents[accidents['lim_velocidade'] != 'DESCONHECIDO']
        accidents = accidents[accidents['tp_pista'] != 'NAO INFORMADO']
        accidents = accidents[accidents['tp_pista'] != 'DESCONHECIDO']
        accidents = accidents.head(76334)
        print(accidents.count())

with zipfile.ZipFile(ZIP_PATH_LOCALITY, 'r') as zip_ref_locality:
    with zip_ref_locality.open(CSV_FILENAME_LOCALITY) as csv_file_locality:
        localities = pd.read_csv(csv_file_locality, sep=';')
        localities = localities[['chv_localidade', 'frota_total', 'frota_circulante']]
        localities = localities.head(76334)
        print(localities.count())


intermediate_dataset = vehicles[['num_acidente', 'tipo_veiculo', 'ind_veic_estrangeiro', 'qtde_veiculos']].copy()
intermediate_dataset['frota_total'] = localities['frota_total'].values
intermediate_dataset['frota_circulante'] = localities['frota_circulante'].values
intermediate_dataset['lim_velocidade'] = accidents['lim_velocidade'].values
intermediate_dataset['tp_pista'] = accidents['tp_pista'].values
print(intermediate_dataset.head())

# Conectar ao MongoDB e inserir dados
db = mongodb_client['trafficAccidents']
collection = db['vehicle']

for _, row in intermediate_dataset.iterrows():
    vehicle = vehicle_entity(row)
    collection.insert_one(vehicle)

print("Dados inseridos com sucesso no MongoDB!")