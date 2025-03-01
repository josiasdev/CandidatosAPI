from models.accident import AccidentBase

def accident_entity_from_csv(entity: dict) -> AccidentBase:
    return {
        "num_acidente": entity['num_acidente'], 
        "chv_localidade": entity['chv_localidade'], 
        "data_acidente": entity['data_acidente'],
        "uf_acidente": entity['uf_acidente'], 
        "dia_semana": entity['dia_semana'], 
        "fase_dia": entity['fase_dia'], 
        "tp_acidente": entity['tp_acidente'], 
        "cond_meteorologica": entity['cond_meteorologica'], 
        "km_via_acidente": entity['km_via_acidente'], 
        "hora_acidente": entity['hora_acidente'], 
        "cond_pista": entity['cond_pista'], 
        "tp_cruzamento": entity['tp_cruzamento'],  
        "tp_pavimento": entity['tp_pavimento'], 
        "tp_curva": entity['tp_curva'], 
        "qtde_acidente": entity['qtde_acidente'], 
        "qtde_acid_com_obitos": entity['qtde_acid_com_obitos'], 
        "qtde_envolvidos": entity['qtde_envolvidos'], 
        "qtde_feridosilesos": entity['qtde_feridosilesos'], 
        "qtde_obitos": entity['qtde_obitos'] 
    }