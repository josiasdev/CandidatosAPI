from models.victim import VictimBase

def victim_entity(entity: dict) -> VictimBase:
    return {
        "num_acidente": str(entity['num_acidente']),
        "chv_localidade": entity['chv_localidade'],
        "data_acidente": entity['data_acidente'],
        "uf_acidente": entity['uf_acidente'],
        "ano_acidente": entity['ano_acidente'],
        "mes_acidente": entity['mes_acidente'],
        "faixa_idade": entity['faixa_idade'],
        "genero": entity['genero'],
        "tp_envolvido": entity['tp_envolvido'],
        "gravidade_lesao": entity['gravidade_lesao'],
        "equip_seguranca": entity['equip_seguranca'],
        "ind_motorista": True if entity['ind_motorista'].upper() == "SIM" else False,
        "susp_alcool": entity['susp_alcool']
    }
