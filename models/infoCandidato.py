# partir do sq_candidato
# fazer uma busca no candidato com sq_candidato egual a sq_candidato
# recuperar esse titulo e salvar no dado

from pydantic import BaseModel

# consulta_cand_complementar_2024.csv
class InfoCandidato(BaseModel):
    id: str # mongodb
    nr_titulo_eleitoral_candidato: str # chave estrangeira do Candidato
    ds_nacionalidade: str
    nm_municipio_nascimento: str
    st_quilombola: bool
    vr_despesa_max_campanha: float
    st_reeleicao: bool # porcentagem de candidatos que tem sim e se reelegem e virse versa
    st_declarar_bens: bool
    st_prest_contas: bool