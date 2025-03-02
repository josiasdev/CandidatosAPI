from models.victim import VictimBase
from datetime import date

def victim_entity(entity: dict) -> VictimBase:
    return {
        "num_acidente": str(entity['num_acidente']),
        "chv_localidade": entity['chv_localidade'],
        "data_acidente": entity['data_acidente'],
        "uf_acidente": entity['uf_acidente'],
        "ano_acidente": str(entity['ano_acidente']),
        "mes_acidente": str(entity['mes_acidente']),
        "mes_ano_acidente": str(entity['mes_ano_acidente']),
        "faixa_idade": entity['faixa_idade'],
        "genero": entity['genero'],
        "tp_envolvido": entity['tp_envolvido'],
        "gravidade_lesao": entity['gravidade_lesao'],
        "equip_seguranca": entity['equip_seguranca'],
        "ind_motorista": True if entity['ind_motorista'].upper() == "SIM" else False,
        "susp_alcool": True if entity['susp_alcool'].upper() == "SIM" else False,
        "qtde_envolvidos": int(entity['qtde_envolvidos']),
        "qtde_feridosilesos": int(entity['qtde_feridosilesos']),
        "qtde_obitos": int(entity['qtde_obitos'])
    }
