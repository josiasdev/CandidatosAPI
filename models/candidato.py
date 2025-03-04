# candidato n:n eleicao
# candidato 1:n canditura n:1 elicao
# candidato 1:1 InfoCandidato

from pydantic import BaseModel
from datetime import datetime

# consulta_cand_2024.csv
class CandidatoCreate(BaseModel):
    nr_titulo_eleitoral_candidato: str # ID - primary-key
    sq_candidato: str # chave estrangeira de candidatura
    nm_candidato: str # nome do candidato
    dt_nascimento: datetime # 16/02/1981
    ds_genero: str # MASCULINO
    ds_grau_instrucao: str # ENSINO MÉDIO COMPLETO
    dc_cor_raca: str # BRANCA
    ds_ocupacao: str # SERVIDOR PÚBLICO MUNICIPAL

class CandidatoBase(CandidatoCreate):
    id_info_candidato: str