from models.locality import LocalityBase
from models.accident import AccidentBase
from typing import List

def locality_entity(entity: dict, accidents: List[AccidentBase]) -> LocalityBase:
    
    related_accidents = [acc for acc in accidents if acc["chv_localidade"] == entity.get('chv_localidade')]

    return LocalityBase(
        chv_localidade=str(entity.get('chv_localidade', '')),
        ano_referencia=str(entity.get('ano_referencia', '')),
        mes_referencia=str(entity.get('mes_referencia', '')),
        mes_ano_referencia=str(entity.get('mes_ano_referencia', '')),
        regiao=str(entity.get('regiao', '')),
        uf=str(entity.get('uf', '')),
        codigo_ibge=str(entity.get('codigo_ibge', '')),  # Garantindo que seja string
        municipio=str(entity.get('municipio', '')),
        regiao_metropolitana=str(entity.get('regiao_metropolitana', '')),
        qtde_habitantes=int(entity.get('qtde_habitantes') or 0),  # Garantindo que seja inteiro
        accidents=related_accidents  # Adicionando os acidentes relacionados
    )
