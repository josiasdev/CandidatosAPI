from models.highway import HighwayBase

def highway_entity(entity: dict) -> HighwayBase:
    return {
        "num_acidente": str(entity['num_acidente']), 
        "tp_rodovia": entity['tp_rodovia'], 
        "cond_pista": entity['cond_pista'], 
        "tp_cruzamento": entity['tp_cruzamento'],  
        "tp_pavimento": entity['tp_pavimento'], 
        "tp_curva": entity['tp_curva'], 
        "lim_velocidade": entity['lim_velocidade'],
        "ind_guardrail": entity['ind_guardrail']
    }