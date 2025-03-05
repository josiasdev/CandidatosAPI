from models.candidato import CandidatoCreate, CandidatoPublic

def candidato_entity(entity: dict) -> CandidatoCreate:
    return {
        "nr_titulo_eleitoral_candidato": entity['nr_titulo_eleitoral_candidato'], 
        "sq_candidato": entity['sq_candidato'], 
        "nm_candidato": entity['nm_candidato'],
        "dt_nascimento": entity['dt_nascimento'], 
        "ds_genero": entity['ds_genero'], 
        "ds_grau_instrucao": entity['ds_grau_instrucao'], 
        "ds_cor_raca": entity['ds_cor_raca'], 
        "ds_ocupacao": entity['ds_ocupacao'] 
    }

def candidato_entity_from_db(entity: dict) -> CandidatoPublic:
    accident = {
        'id_info_candidato': str(entity['id_info_candidato']),
        **candidato_entity(entity)
    }
    
    return accident

def candidato_entities_from_db(entities: list) -> list[CandidatoPublic]:
    return [candidato_entity_from_db(entity) for entity in entities]