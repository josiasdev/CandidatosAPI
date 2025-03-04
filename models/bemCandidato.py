# candidato 1:n bens
# bem 1:n candidaturas

# partir do sq_candidato
# fazer uma busca no candidato com sq_candidato egual a sq_candidato
# recuperar esse titulo e salvar no dado

from datetime import datetime
from pydantic import BaseModel

# bem_candidato.csv
class BemCandidato(BaseModel):
    id: str # mongodb
    nr_titulo_eleitoral_candidato: str
    sq_candidato: str # foreign-key - Candidatura
    nr_ordem_bem_candidato: int
    ds_tipo_bem_candidato: str
    ds_bem_candidato: str
    vr_bem_candidato: float
    dt_ult_atual_bem_candidato: datetime
    hh_ult_atual_bem_candidato: datetime