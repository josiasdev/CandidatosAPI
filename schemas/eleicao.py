from models.eleicao import EleicaoBase
from datetime import datetime

def eleicao_entity(entity: dict) -> EleicaoBase:
    return EleicaoBase(
        cd_eleicao=str(entity['CD_ELEICAO']),  # Transformando para string
        ds_eleicao=entity['DS_ELEICAO'],  # Descrição da eleição
        dt_eleicao=datetime.strptime(entity['DT_ELEICAO'], '%d/%m/%Y'),  # Convertendo string para datetime
        ano_eleicao=str(entity['ANO_ELEICAO']),  # Convertendo para string
        cd_tipo_eleicao=str(entity['CD_TIPO_ELEICAO']),  # Convertendo para string
        nm_tipo_eleicao=entity['NM_TIPO_ELEICAO'],  # Nome do tipo de eleição
        tp_abrangencia=entity['TP_ABRANGENCIA'],  # Tipo de abrangência da eleição
        nr_turno=str(entity['NR_TURNO']),  # Convertendo para string
        qt_vaga=entity['QT_VAGA'],  # Quantidade de vagas
    )
