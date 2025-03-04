from pydantic import BaseModel
from datetime import datetime

# consulta_cand_2024.csv + consulta_vagas_2024.csv
class Eleicao(BaseModel):
    #Eleicao
    cd_eleicao: str # id eleicao
    ds_eleicao: str # descricao eleicao
    dt_eleicao: datetime # data eleicao
    ano_eleicao: int
    cd_tipo_elicao: str
    nm_tipo_eleicao: str
    tp_abrangencia: str # tipo abrangencia eleicao
    dt_posse: datetime # from vagas - NAO TEM no Candidato
