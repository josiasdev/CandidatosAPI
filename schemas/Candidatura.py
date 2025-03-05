from models.Candidatura import CandidaturaCreate, CandidaturaPublic

def candidatura_entity(entity: dict) -> CandidaturaCreate:
    return {
        "sq_candidato": entity["SQ_CANDIDATO"],
        "nm_candidato": entity["NM_CANDIDATO"],
        "cd_eleicao": entity["CD_ELEICAO"],
        "sg_uf": entity["SG_UF"],
        "ds_cargo": entity["DS_CARGO"],
        "nr_candidato": entity["NR_CANDIDATO"],
        "nr_partido": entity["NR_PARTIDO"],
        "sg_partido": entity["SG_PARTIDO"],
        "nm_partido": entity["NM_PARTIDO"],
        "nr_turno": entity["NR_TURNO"],
        "tp_agremiacao": entity["TP_AGREMIACAO"],
        "ds_sit_tot_turno": entity["DS_SIT_TOT_TURNO"],
        "ds_tp_motivo": entity.get("DS_TP_MOTIVO"),  # Pode ser None
        "ds_motivo": entity.get("DS_MOTIVO")  # Pode ser None
    }

def candidatura_entity_from_db(entity: dict) -> CandidaturaPublic:
    candidatura = {
        "id": str(entity["_id"]),
        **candidatura_entity(entity)
    }
    return CandidaturaPublic(**candidatura)

def candidatura_entities_from_db(entities: list) -> list[CandidaturaPublic]:
    return [candidatura_entity_from_db(entity) for entity in entities]
