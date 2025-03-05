from models.BensCandidato import BensCandidatoCreate, BensCandidatoPublic

def bens_candidato_entity(entity: dict) -> BensCandidatoCreate:
    return {
        "nr_titulo_eleitoral_candidato": entity['NR_TITULO_ELEITORAL_CANDIDATO'],
        "sq_candidato": entity['SQ_CANDIDATO'],
        "nr_ordem_bem_candidato": entity['NR_ORDEM_BEM_CANDIDATO'],
        "ds_tipo_bem_candidato": entity['DS_TIPO_BEM_CANDIDATO'],
        "ds_bem_candidato": entity['DS_BEM_CANDIDATO'],
        "vr_bem_candidato": entity['VR_BEM_CANDIDATO'],
        "dt_ult_atual_bem_candidato": entity['DT_ULT_ATUAL_BEM_CANDIDATO'],
        "hh_ult_atual_bem_candidato": entity['HH_ULT_ATUAL_BEM_CANDIDATO']
    }

def bens_candidato_entity_from_db(entity: dict) -> BensCandidatoPublic:
    bens_candidato = {
        'id': str(entity['_id']),
        **bens_candidato_entity(entity)
    }
    
    return BensCandidatoPublic(**bens_candidato)

def bens_candidato_entities_from_db(entities: list) -> list[BensCandidatoPublic]:
    return [bens_candidato_entity_from_db(entity) for entity in entities]