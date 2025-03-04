from pydantic import BaseModel
from datetime import datetime

# consulta_cand_2024.csv + consulta_vagas_2024.csv
class Eleicao(BaseModel):
    #Eleicao
    # Pegar somente 1 de cada código
    cd_eleicao: str # id eleicao, único por eleição e por turno
    ds_eleicao: str # descricao eleicao
    dt_eleicao: datetime # data eleicao
    ano_eleicao: int
    cd_tipo_eleicao: str
    nm_tipo_eleicao: str
    tp_abrangencia: str # tipo abrangencia eleicao
    nr_turno: str
    dt_posse: datetime # from vagas - NAO TEM no Candidato, tá em vagas